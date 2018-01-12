---
layout: post
title: Dipping my toes into utility CSS
date: 2018-01-12 00:00:00 +0000
excerpt: ''
tags: []
---
This is a quick

## Basic utility classes

```
.br-pill {
  border-radius: 9999px;
}

.dib {
  display: inline-block;
}

.w1 {
  width: 1em;
}

.h1 {
  height: 1em;
}

.bg-primary {
  background-color: $primary;
}
```

## Simple component using `@extend`

```
.ind {
  @extend .br-pill;
  @extend .dib;
  @extend .w1;
  @extend .h1;
}

.ind--primary {
  @extend .bg-primary;
}
```

## Rendered CSS

```
.br-pill, .ind {
  border-radius: 9999px;
}

.dib, .ind {
  display: inline-block;
}

.w1, .ind {
  width: 1em;
}

.h1, .ind {
  height: 1em;
}

.bg-primary, ind--primary {
  background-color: #59a33f;
}
```