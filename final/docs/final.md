# Mathematical formulation of the problem:

Let $V$ be the set of n students.

$$V = \{v_{1}, v_{2}, v_{3} \dots v_{n}\}$$

Let $E$ be the set of matchups.

$(v_{a}, v_{b}) \in E$ means that student $v_{a}$'s paper is paired against player $v_{b}$'s paper.

$$E \subset V \times V \text{ where } \forall (v_{a}, v_{b}) \in E, v_{a} \neq v_{b}$$ 

Let $A$ be the set of all assignments.

$(v_{i},v_{j},v_{k}) \in A$ means that student $v_{i}$ marks the matchup $(v_{j}, v_{k}) \in E.$

$$A \subset E \times V \text{ where } \forall (v_{i},v_{j},v_{k}) \in A, v_{i} \neq v_{j} \neq k$$

Each student $v \in V$ has a score $t(v)$.

$$t: V \rightarrow [0, 1]$$

We can define a relation $\preceq_{t}$ over $V$. 

$$\forall v, v' \in V, v \preceq_{t} v' \text{ iff } t(v) \leq t(v')$$

## Our problem is as follows:

Given $V, E, A$ find a scoring function $t'(v)$ such that the total order defined by $\preceq_{t'}$ is 'close to' the total order defined by $\preceq_{t}$.

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

## How do we obtain $A$?

Assuming we're in charge of the matchup assignments. Then there are certain properties that we would like to satisfy.

1. Each student does not mark their own paper.
2. Avoid giving a grader too many of a single student's matchups.
3. Keep the workload of each student fairly even.

Condition 1\. 

This is already handled by the definition of $A$.

Condition 2\. 

Let's say player 2 is assigned the matchups: (1,3), (3, 5), (3, 4) and (6, 3). In this case a lot of player 3's matches are concentrated in player 2's hands. If player 2 is a poor student then we will not have much useful information on player 3's skill.

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

## Decision Variables

For each assignment $(i,j,k) \in A$, we define a decision variable $X_{i,j,k} \in \{0, 1\}$.

If $X_{i,j,k} = 1$ then the matchup $(j,k)$ is assigned to player $i$.
If $X_{i,k,k} = 0$ then the matchup $(j,k)$ is not assigned to player $i$.

## Constraints

$\forall (j,k) \in E, \sum_{v \in V} X_{v,j,k} = 1$

Let $f(v) = \sum_{(j, k) \in E} X_{v, j, k}$

$\forall (a, b) \in V \times V, a \neq b, |f(a) - f(b)| \leq 1$


## Objective function

Let $s_{a}(b) = \sum_{v \in V} X_{a,b,v}$

$\text{ minimise }  max(\{s_{a}(b) | (a, b) \in V \times V, a \neq b\})$


## Something to think about

In our first model of students grading, we assumed that marking skill was a function of player skill.
Specifically grading\_skill = 0.5 * player\_skill + 0.5
This is a mapping from [0 - 1] to [0.5 - 1]. This assumes that players with a score of 0 are purely guessing.

However, let's take a maths exam. If a player got 0% on the exam, and was 100% confident in their answers, and each question was multiple choice. Then they would always mark the matchup incorrectly. In this case grading\_skill = player\_skill.


But what about a non-objective marking. For example a history essay. In this case would we keep the same model? Would the student guess?

Also would a student who got 0% on a maths exam be 100% confident on their paper?
