---
title: "Implementing a system for tournament peer grading"
author: 
    - "Author: Ricky Chu"
    - "Supervisor: Richard Booth"
geometry:
    - margin=30mm
---

# Mathematical formulation of the problem:

Let $V$ be the set of n students.

$$V = \{v_{1}, v_{2}, v_{3} \dots v_{n}\}$$

Let $E$ be the set of matchups.

$(v_{a}, v_{b}) \in E$ means that student $v_{a}$'s paper is paired against player $v_{b}$'s paper.

$$E \subset V \times V \text{ where } \forall (v_{a}, v_{b}) \in E, v_{a} \neq v_{b}$$ 

Let $A$ be a set of assignments.

$(v_{i},v_{j},v_{k}) \in A$ means that student $v_{i}$ marks the matchup $(v_{j}, v_{k}) \in E.$

$$A \subset E \times V \text{ where } \forall (v_{i},v_{j},v_{k}) \in A, v_{j} \neq v_{i} \neq v_{k}$$

Each student $v \in V$ has a score $t(v)$.

$$t: V \rightarrow [0, 1]$$

We can define a relation $\preceq_{t}$ over $V$. 

$$\forall v, v' \in V, \quad v \preceq_{t} v' \text{ iff } t(v) \leq t(v')$$

## Our problem is as follows:

Given $V, E, A$ find a relation $\preceq_{t'}$ such that the preorder defined by $\preceq_{t'}$ is 'close to' the preorder defined by $\preceq_{t}$.

## For example let's take 4 students

$$V = \{a, b, c, d\}$$

$$E = \{(a,b), (a,c), (a,d), (b,c), (b,d), (c,d)\}$$

$$
\begin{aligned}
A = \{ & (c, a, b), (d, a, b), (b, a, c), (d, a, c), \\
       & (b, a, d), (c, a, d), (a, b, c), (d, b, c), \\
       & (a, b, d), (c, b, d), (a, c, d), (b, c, d) \}
\end{aligned}
$$

$$
\begin{aligned}
& t(a) = 0.72 \\
& t(b) = 0.32 \\
& t(c) = 0.95 \\
& t(d) = 0.45 \\
\end{aligned}
$$

$$ b \preceq_{t} d \preceq_{t} a \preceq_{t} c $$

## Closeness?

In order to measure closeness between 2 preorders we need some sort of distance metric. One common metric is the Kendall tau distance. This measures the number of differing pairs in the 2 preorders.

For example let's take the relations $\preceq_{t}$ and $\preceq_{t'}$ over $V = \{a, b, c\}$

$$ b \preceq_{t} d \preceq_{t} a \preceq_{t} c $$
$$\preceq_{t} = \{(b,d),(b,a),(b,c),(d,a),(d,c),(a,c),(a,a),(b,b),(c,c),(d,d)\}$$

$$ c \preceq_{t'} b \preceq_{t'} a \preceq_{t'} d $$
$$\preceq_{t'} = \{(c,b),(c,a),(c,d),(b,a),(b,d),(a,d),(a,a),(b,b),(c,c),(d,d)\}$$

The set of differing pairs is

$$\preceq_{t} \setminus \preceq_{t'} = \{(b,c), (d,a), (d,c), (a,c)\}$$

So the Kendall Tau distance is 
$$K_{d}(\preceq_{t}, \preceq_{t'}) = |\preceq_{t} \setminus \preceq_{t}| = 4 $$

$$|\preceq_{t} \setminus \preceq_{t'}| = |\preceq_{t'} \setminus \preceq_{t}|$$

If we let $n$ be the number of items in our preorders, and the first preorder is the reverse of the second preorder, then $\frac{n(n-1)}{2}$ is the Kendall Tau distance between them. This corresponds to the situation where all the pairs are differing.

Therefore, the normalised Kendall tau distance $K_{n}$ is

$$K_{n} = \frac{K_{d}}{\frac{n(n-1)}{2}} = \frac{2K_{d}}{n(n - 1)}$$

# How do we obtain $A$?

Assuming we're in charge of the matchup assignments. Then there are certain properties that we would like to satisfy.

1. Each student does not mark their own paper.
2. Avoid giving a grader too many of a single student's matchups.
3. Keep the workload of each student fairly even.

Condition 1\. 

This is already handled by the definition of $A$.

Condition 2\. 

Let's say player 2 is assigned the matchups: (1,3), (3, 5), (3, 4) and (6, 3). In this case a lot of player 3's matches are concentrated in player 2's hands. If player 2 is a poor student then we will not have much useful information to infer player 3's skill.

Condition 3\. 

If player 1 is assigned the matchups: 

- (2,3) 

and player 2 is assigned the matchups

- (1,4)
- (3,1)
- (5,3)
- (5,1)

Then player 2 is marking a lot more matchups that player 1. Which would be an unfair workload.

To solve this problem of matchup assignments we can turn to a Mixed Integer Linear Programming model.

## The MILP Model for paper distribution.

### Decision Variables

For each assignment $(i,j,k) \in A$, we define a decision variable $X_{i,j,k} \in \{0, 1\}$.

If $X_{i,j,k} = 1$ then the matchup $(j,k) \in E$ is assigned to player $i$.

If $X_{i,k,k} = 0$ then the matchup $(j,k) \in E$ is not assigned to player $i$.

### Constraints

Let's define a function $f(v)$. This takes in a student $v$ and returns the sum of all the decision variables that represents a matchup being assigned to $v$. In other words it's the total number of matchups student $v$ marks.

$$f(v) = \sum_{(j, k) \in E} X_{v, j, k}$$

To satisfy condition 3 we can add the following constraint. For every pair of students, the number of matchups assigned to them cannot differ by more than 1[^1]. 

[^1]: You may wonder why we don't make it equal to 1. This is because for many graphs it'll be infeasible. For example take the graph $K_{4}$. $K_{4}$ has $6$ edges and $4$ nodes. It's impossible to create an assignment for $K_{4}$ where each node has the same number of matchups to mark.

$$\forall (a, b) \in V \times V, a \neq b, \quad |f(a) - f(b)| \leq 1$$

This next constraint ensures that every matchup in $E$ gets assigned to at least one player.

$$\forall (j,k) \in E, \quad \sum_{v \in V} X_{v,j,k} \geq 1$$

### Objective function

Let's define a function $s(a, b)$. This takes in 2 students $a$ and $b$, and returns the number of times a matchup containing $b$ is assigned to $a$. For example if $A = \{(a, b, c), (a, b, d), (a, f, b), (a, j, k)\}$, then $s(a, b) = 3$

$$s(a,b) = \sum_{v \in V} X_{a,b,v} + X_{a, v, b}$$

We can now define out objective function. This corresponds to condition 2. Which avoids concentrating all of player $b$'s matches in the hands of player $a$.

$$\text{minimise }  max(\{s(a,b) | (a, b) \in V \times V, a \neq b\})$$

## $abs$ and $max$ in a linear program?

$abs$ and $max$ aren't linear functions. So they can't be used in a linear programming model. However, there are tricks we can employ with slack variable to implement these.

Let's say we have 2 decision variables $X_{1}$ and $X_{2}$. In order to find $max(X_{1}, X_{2})$ we'll create a slack variable $M$.

Next we'll add the constraints:

$$M \geq X_{1}$$
$$M \geq X_{2}$$

$M$ will now be larger than (or equal to) $max(X_{1}, X_{2})$. However, if we minimise over $M$, then $M$ will be restricted to be equal to the value of $max(X_{1}, X_{2})$. 

To find $abs(X_{1}, X_{2})$ we'll create another slack variable $A$.

We can then add the constraints:

$$A \geq X_{1} - X_{2}$$
$$A \geq X_{2} - X_{1}$$

$A$ will be larger than (or equal to) $abs(X_{1}, X_{2})$ We can now apply the same trick as $max$. In our specific case we don't need to do that since we have the constraint $A \leq 1$.

# Ranking methods

Now that we've obtained a set of assignments 

## Something to think about

In our first model of students grading, we assumed that marking skill was a function of player skill.
Specifically grading\_skill = 0.5 * player\_skill + 0.5
This is a mapping from [0, 1] to [0.5, 1]. This assumes that players with a score of 0 are purely guessing.

However, let's take a maths exam. If a player got 0% on the exam, and was 100% confident in their answers, and each question was multiple choice. Then they would always mark the matchup incorrectly. In this case grading\_skill = player\_skill.

But what about a non-objective marking. For example a history essay. In this case would we keep the same model? Would the student guess?

Also would a student who got 0% on a maths exam be 100% confident on their paper?

Maybe we could have some sort of in-between? I.e. mapping [0 - 1] to [0.2 - 1]?

Given (A, B, C). Could the probability depend on the difference between B's and C's score?

## Ideas for turning it into a website?

Little about section with explanation + link to repo + paper 

Main section will have 2 options:

- Full thing w/ paper distribution
- Little DSL that lets you input pairs and gives you a ranking approximation

HTMX for the frontend.
FastAPI for the backed.
