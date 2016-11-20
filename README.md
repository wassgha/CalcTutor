# Calculus Tutor
*for Integration and Differentiation Exercises*

**This is a work-in-progress Intelligent Tutor System for calculus courses built with [Django](https://www.djangoproject.com/) and Python.** 

![Math Tutor](http://i.imgur.com/l9VSNeS.png)

## Background

We are trying to improve on existing homework delivery platforms (ex. WebWorK) by extending the randomization of questions beyond constants to the dynamic generation of different functions autonomously. 

In calculus, we are exploiting the fact that students learn a short list of differentiation and integration rules and are expecting to apply nothing more than these in many problems.

This allows us to randomly string together solution rules in order to produce solvable problems of appropriate difficulty and complexity. We represent the problems using weighted expression trees. 

## The Platform

To implement this, we created a general purpose intelligent tutoring platform.  Exercises are stored in a database and each exercise is defined by generic functions and variables such as the input method, the prompt (returned in HTML) and a method that verifies student input and returns feedback and hints accordingly.

We also had to implement a responsive Mathematical On-screen Keyboard that converts student input to LaTeX code which can be interpreted by the platform. To do so, we used jQuery and HTML complemented by `MathQuill` and `MathJax` (to display the input). The resulting product is as shown below :

![Imgur](http://i.imgur.com/Wx10s29.png)

## Research Progress

Both the generation of integration and differentiation questions have been implemented at this stage. We have also implemented the validation algorithm that says whether a student's input is the right answer or not.

We are now looking to build a database where data is collected from student subjects' answers to the generated questions. This will allow us to monitor each student's progress using the tutor with different difficulties of questions. It will also give us an idea about common mistakes. Since we also record the expression tree for each generated question, we can proceed to analyze the steps that challenge students the most.

We anticipate to use the collected responses as training data for learning how to rate problems, say on a multiparameter Item Response Theory scale. The tree retains the semantic information about the problem structure, so should give a good model for automated rating. (Eventually, the hope is to provide free automated test banks.) We also gain the ability to require or exclude certain rules during problem generation.

## The Algorithm

Our algorithm is based on building an expression tree contrained by the rules that students are able to solve.

In order to implement the algorithm, we started with so-called production rules corresponding to each possible problem step, along with solution rules and prior estimates of difficulty weighting. For calculus, these are elementary functions, such as `FUNCTION->(sin(x))`, which provide all the terminal symbols, as well as grammar-type rules, such as `FUNCTION->COMPOSE(FUNCTION, FUNCTION)`. Differential Equation problems are likely to follow a similar model. Linear Algebra probably requires more thought.

As an example, one could produce problems with the template "Find the inverse Laplace transform of F(s)." `F(s)` would be randomly built up from pieces and steps that the student should know how to handle. By providing corresponding solution production rules, `f(t)` may be produced automatically, along with a step-by-step solution amenable to providing hints. It is then routine to check the user response against `f(t)` via a small number of random test points.

## Contact us
* Wassim Gharbi (Lafayette College '19) 

> Email : <gharbiw@lafayette.edu>

* Huy Nguyen (Lafayette College '18) 

> Email : <nguyenha@lafayette.edu>
