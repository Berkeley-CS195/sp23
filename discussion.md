---
layout: page
released: true
title: "CS H195: Honors Social Implications of Computer Technology"
---

Jump on this page:

- CS H195 Syllabus: [link](#cs-h195-syllabus)
- Discussions, Readings, and Resources: [link](#cs-h195-resources)

## Readings Table of Contents

{% assign readings = site.csH195_discussions | sort: 'date' %}

| Date  | Discussion | Topic                                 | Slides | Readings |
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

***

CS H195 discussions complement and supplement the topics presented in CS 195
lecture series. Students are expected to engage at a deeper level with the
assigned weekly readings and be prepared to engage in thoughtful and
constructive discussions around the course material. Where applicable, we will
invite guest speakers from industry and academia to present their work and to
participate in discussions alongside students. CS H195 will encourage students
to go beyond thinking about computer technology as solely an engineering
problem but instead viewing it holistically from the perspective of social
sciences, legal studies, policymaking, equity, and inclusion.

**CS H195 time**: See the sidebar.

## CS H195 Syllabus

### Course components

**To pass this course, you must:**

- Attend most <b>CS 195 lectures</b>,
- Be present at all <b>CS H195 discussions</b>,
- Submit all <b>CS 195/H195 reading assignments and surveys</b>, and
- Complete passing work on all <b>CS H195 projects</b>.

**Course Policies**: We understand things come up during the semester and
synchronous participation may not always be possible. This course is P/NP, and
we will make every effort to work with you to help you pass this course.

- CS 195 lecture and survey completion will be graded according to CS 195 course policies (see sidebar).
- Attendance is expected at every CS H195 discussion. If you need to miss any, we'd appreciate early notice so we can assign you make up work.
  - Weeks 1 and 2: Because of beginning of semester class shuffling, we did not take Week 1 attendance. However, we expect you to do the readings and submit them a week from when you first start attending H195 discussions.
- Most projects are group work with in-class presentations.

### Projects

Intead of the CS 195 essays, this semester we are building new H195 project assignments.
This semester, we are trying some new assignments for CS H195. We appreciate your working with us to design this course, and we welcome your feedback!!

**All dates below are subject to change.**

|       | Projects | Estimated duration | Project Due  | Links                    |
| ----- | ------ | ----- | --- |
| 1     | Social Media Simulation | 1-2 weeks | Fri 2/24 | [link][proj1]      |
| 2     | Teaching Computing in the News | ~3 weeks | Fri. 3/24 |       |
| 3     | Technology and the Community   | ~4 weeks | Fri. 4/28 |       |

[proj1]: assignments/h195-proj1.md

<b>1. Social Media Simulation</b>: (individual)  Analyze the dynamics of
information bubbles and polarization in social network models. Submit a writeup.
<br/>

<b>2. Teaching Computing in the News</b>: (groups) What H195 discussion would
you run? Build a lesson plan for a 50-minute discussion for (future) H195
students to engage critically with the social context of a particular computing
technology. We will provide readings on pedagogical practices.

- 3/10: Select a topic and readings.
- 3/17: Design preparation exercise, discussion exercise.
- 3/24: Identify takewaways, present in class.


<b>3. Technology and the Community</b>: (groups) Engage with the community to
inform impacts of technology on particular groups of people. This project is
*open-ended* and we are hoping that we can co-design this assessment with
you. What do you want to have learned from this class? What kind of community
do you want to participate in?

- 4/14: Community selection, interview plan.
- 4/28: Present on findings from interviews.

More details on each assignment will be provided as soon as we know them.

### Course Description

CS H195 is a 3-unit course. In addition to attending the regular weekly lecture,
students will participate in weekly discussions and write reading responses,
lead discussions and prepare presentations informed by their understanding of
the material, and engage in a series of experiential and real-world assignments.

## CS H195 Resources

{% for r in readings reversed %}
  {%- if r.readings_released -%}
    {{ r }}
  {%- endif %}
{% endfor %}
