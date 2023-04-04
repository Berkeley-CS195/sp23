---
layout: page
released: true
title: Topics, Readings, and Assignments
---

{% assign readings = site.cs195_readings | sort: 'date' %}

| Date  | Lecture | Topic                                 | Slides | Readings |
|-------|-------- | --------------------------------------|--------| ----------- |
{% for r in readings -%}
  | {{ r.date | date: "%m/%d" }} | {{ r.number }} | {{ r.title }} |
  {%- if r.slides.released -%}
    [link]({{ r.slides.link }})
  {%- else -%}
    link
  {%- endif -%}
  |
  {%- if r.readings_released -%}
    [jump](#lecture{{ r.number }})
  {%- else -%}
    jump
  {%- endif %}
{% endfor %}

## Readings

Readings are "required", "recommended", or "extra". Required readings should be
done before class for the discussion to make sense. Recommended readings will be
used as sources in lecture, but we won't assume you've read them.

More information about the assignments, including the essays, can be found on
the Assignments page in the sidebar.

{% for r in readings reversed %}
  {%- if r.readings_released -%}
    <hr>
    {{- r -}}
  {%- endif %}
{% endfor %}
