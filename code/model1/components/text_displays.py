import streamlit as st
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import json

def show_code_block(code, language="python", title=None, show_line_numbers=True):
    """显示代码块"""
    if title:
        st.subheader(title)
    
    # 显示代码
    st.code(code, language=language, line_numbers=show_line_numbers)
    
    # 提供复制代码的按钮
    st.download_button(
        label="复制代码",
        data=code,
        file_name=f"code.{language}",
        mime="text/plain",
    )

def show_api_response(response, title="API响应"):
    """显示API响应内容"""
    st.subheader(title)
    
    # 对响应类型进行检查
    if isinstance(response, dict) or isinstance(response, list):
        # JSON响应
        st.json(response)
        
        # 提供下载选项
        st.download_button(
            label="下载为JSON文件",
            data=json.dumps(response, indent=2, ensure_ascii=False),
            file_name="response.json",
            mime="application/json",
        )
    elif isinstance(response, str):
        # 检查是否为HTML响应
        if re.search(r'<!DOCTYPE html>|<html', response, re.IGNORECASE):
            show_html_preview(response, title="HTML响应预览")
        else:
            # 纯文本响应
            st.text_area("响应内容", value=response, height=300)
            
            # 提供下载选项
            st.download_button(
                label="下载为文本文件",
                data=response,
                file_name="response.txt",
                mime="text/plain",
            )
    else:
        # 其他类型响应
        st.write("无法预览的响应类型")
        st.write(f"类型: {type(response)}")

def show_html_preview(html_content, title="HTML预览"):
    """显示HTML内容预览"""
    st.subheader(title)
    
    # 创建选项卡
    tab1, tab2, tab3 = st.tabs(["渲染视图", "源代码", "结构分析"])
    
    with tab1:
        # 使用HTML组件渲染
        st.components.v1.html(html_content, height=500, scrolling=True)
    
    with tab2:
        # 显示源代码
        with st.expander("查看完整HTML源码"):
            st.code(html_content, language="html", line_numbers=True)
    
    with tab3:
        # 解析HTML并显示结构
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 提取标题和元信息
        st.write("#### 页面信息")
        
        title_tag = soup.find("title")
        title_text = title_tag.text if title_tag else "无标题"
        st.write(f"**标题**: {title_text}")
        
        meta_tags = soup.find_all("meta")
        if meta_tags:
            st.write("**Meta标签**:")
            meta_info = []
            for meta in meta_tags:
                name = meta.get("name", meta.get("property", ""))
                content = meta.get("content", "")
                if name and content:
                    meta_info.append({"名称": name, "内容": content})
            
            if meta_info:
                st.dataframe(pd.DataFrame(meta_info))
        
        # 统计各类元素
        st.write("#### 元素统计")
        elements = {
            "链接 (a)": len(soup.find_all("a")),
            "图片 (img)": len(soup.find_all("img")),
            "表格 (table)": len(soup.find_all("table")),
            "表单 (form)": len(soup.find_all("form")),
            "输入框 (input)": len(soup.find_all("input")),
            "按钮 (button)": len(soup.find_all("button")),
            "脚本 (script)": len(soup.find_all("script")),
            "样式 (style/link)": len(soup.find_all("style")) + len(soup.find_all("link", rel="stylesheet")),
            "标题 (h1-h6)": sum(len(soup.find_all(f"h{i}")) for i in range(1, 7)),
            "段落 (p)": len(soup.find_all("p")),
            "列表 (ul/ol)": len(soup.find_all("ul")) + len(soup.find_all("ol")),
        }
        
        st.dataframe(pd.DataFrame({"元素类型": list(elements.keys()), "数量": list(elements.values())}))
        
        # 查看所有链接
        links = soup.find_all("a")
        if links:
            st.write("#### 页面链接")
            link_info = []
            for link in links:
                href = link.get("href", "")
                text = link.text.strip()
                if href:
                    link_info.append({"链接文本": text or "[无文本]", "URL": href})
            
            if link_info:
                with st.expander(f"查看所有链接 ({len(link_info)})"):
                    st.dataframe(pd.DataFrame(link_info))
        
        # 查看所有图片
        images = soup.find_all("img")
        if images:
            st.write("#### 页面图片")
            image_info = []
            for img in images:
                src = img.get("src", "")
                alt = img.get("alt", "")
                if src:
                    image_info.append({"图片描述": alt or "[无描述]", "图片URL": src})
            
            if image_info:
                with st.expander(f"查看所有图片 ({len(image_info)})"):
                    st.dataframe(pd.DataFrame(image_info))

def show_tutorial(title, sections):
    """显示教程内容，支持分段展示"""
    st.title(title)
    
    # 处理教程目录
    if len(sections) > 1:
        st.subheader("目录")
        for i, section in enumerate(sections):
            st.write(f"{i+1}. {section['title']}")
        
        st.divider()
    
    # 显示教程内容
    for i, section in enumerate(sections):
        with st.expander(f"{i+1}. {section['title']}", expanded=i==0):
            if "content" in section:
                st.markdown(section["content"])
            
            if "code" in section:
                show_code_block(
                    section["code"], 
                    language=section.get("language", "python"),
                    title=section.get("code_title", "代码示例")
                )
            
            if "image" in section:
                st.image(section["image"], caption=section.get("image_caption", ""))
            
            if "demo" in section and callable(section["demo"]):
                st.subheader("交互演示")
                section["demo"]()

def show_info_card(title, content, icon=None, is_expanded=False):
    """显示信息卡片"""
    if icon:
        title = f"{icon} {title}"
    
    with st.expander(title, expanded=is_expanded):
        st.markdown(content)

def show_steps(steps, title="操作步骤"):
    """显示步骤指引"""
    st.subheader(title)
    
    # 显示每个步骤
    for i, step in enumerate(steps):
        step_title = step.get("title", f"步骤 {i+1}")
        step_content = step.get("content", "")
        step_code = step.get("code", None)
        step_image = step.get("image", None)
        
        col1, col2 = st.columns([1, 10])
        
        with col1:
            st.markdown(f"### {i+1}")
        
        with col2:
            st.markdown(f"**{step_title}**")
            st.markdown(step_content)
            
            if step_code:
                st.code(step_code, language=step.get("language", "python"))
            
            if step_image:
                st.image(step_image, caption=step.get("image_caption", ""))

def show_markdown_file(content, title=None):
    """显示Markdown文件内容"""
    if title:
        st.title(title)
    
    # 渲染Markdown内容
    st.markdown(content)

def show_warning_box(message, title=None):
    """显示警告框"""
    warning_box = st.warning(message)
    if title:
        warning_box.title = title
    return warning_box

def show_success_box(message, title=None):
    """显示成功提示框"""
    success_box = st.success(message)
    if title:
        success_box.title = title
    return success_box

def show_error_box(message, title=None):
    """显示错误提示框"""
    error_box = st.error(message)
    if title:
        error_box.title = title
    return error_box

def show_info_box(message, title=None):
    """显示信息提示框"""
    info_box = st.info(message)
    if title:
        info_box.title = title
    return info_box