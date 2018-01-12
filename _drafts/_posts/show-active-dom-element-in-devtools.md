---
title: Show active DOM element in DevTools
tags:
- til
- DevTools
- JavaScript
date: 2018-01-11 00:00:00 +0000
excerpt: How to show the currently active DOM element in the console of Chrome DevTools.
publication: ''
link: ''
external: false
---
Sometimes you find yourself trying to identify I weird bug in a piece of UI and often DevTools comes to the rescue to help you out. 

I was experiencing an issue this week where a UI element would click and get focus without pressing it twice, it only occurred in a particular scenario and it was getting frustrating.

Using DevTools and particulary the Console 

![A screenshot of a website with Chrome developers tools open with the console showing.](/assets/uploads/2018/01/11/devtools-active-element.png "An example of the the document.activeElement in use")

    document.activeElement