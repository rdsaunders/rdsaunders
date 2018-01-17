---
layout: post
title: Identifying visual density and hierarchy using the CSS filter property
date: 2018-01-17 00:00:00 +0000
excerpt: Use the filter CSS property as a quick acid test to see which elements of
  your site or application may be getting more attention.
tags:
- CSS
- Design
---
When building an application, you can't always put you finger to why something feels wrong in the design, often it can be down to the visual density or hierarchy of the elements on the screen.
 
Using the filter CSS property can provide a way to create a quick acid test to see which elements of your site or application may be getting more attention.

```
html {
		filter: blur(5px) grayscale(1);
}
```