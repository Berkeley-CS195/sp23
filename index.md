---
layout: page
released: true
title: Topics, Readings, and Assignments
---

**Enrollment**: (Update 1/28): The EECS department has submitted the expansion
request to the College of Engineering and things seem reasonably positive; we
are waiting for final approval to allow all waitlisted and concurrent
enrollment students, as well as those non-EECS students.

In the meantime, if you are still waitlisted/not enrolled in the class, please
email Ethan so we can manually add you to bCourses. Thanks for your patience
and understanding. You can also join the Ed for further course announcements:
[Ed join link](https://edstem.org/us/join/E8BdJn) This will be refreshed after
the final course adjustment deadline passes.

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
    {{ r }}
  {%- endif %}
{% endfor %}
