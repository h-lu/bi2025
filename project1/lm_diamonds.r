library(tidyverse)
library(broom)
library(gapminder)

china <- gapminder %>%
  filter(country == "China")

china

ggplot(china, aes(x = year, y = gdpPercap)) +
  geom_line() +
  geom_smooth(method = "lm", se = FALSE)

lm_china <- lm(gdpPercap ~ year, data = china)
tidy(lm_china)
glance(lm_china)

gapminder %>%
  distinct(country)

ggplot(gapminder, aes(x = year, y = gdpPercap, group = country)) +
  geom_line()



filtered_country <- gapminder %>%
  group_nest(country) %>%
  mutate(
    result = map(data, ~lm(gdpPercap ~ year, data = .x)) %>% map(tidy)
  ) %>%
  select(-data) %>%
  unnest(result) %>%
  filter(term == "year") %>%
  filter(p.value < 0.05, estimate < 0)

gapminder %>%
  semi_join(filtered_country, by = "country") %>%
  distinct(country, continent)


gapminder %>%
  group_nest(country) %>%
  mutate(
    result = map(data, ~lm(gdpPercap ~ year, data = .x)) %>% map(tidy)
  ) %>%
  select(-data) %>%
  unnest(result) %>%
  filter(term == "year") %>%
  ggplot(aes(x = fct_reorder(country, estimate), y = estimate, fill = p.value < 0.05)) +
  geom_col() +
  coord_flip()
