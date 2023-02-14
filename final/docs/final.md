# Mathematical formulation of the problem:

Let $V$ be the set of n students.

$V = \{1, 2, 3 \dots n\}$

Let $E$ be the set of matchups.

$E \subset V \times V$ where $\forall (a, b) \in E, a \neq b$

$(a, b) \in E$ means that student $a$'s paper is paired against player $b$'s paper.

Let $A$ be the set of all assignments.

$A \subset E \times V$ where $\forall (i,j,k) \in A, i \neq j \neq k$

$(i,j,k) \in A$ means that student $i$ marks the matchup $(j, k) \in E.$

Each student $v \in V$ has a score $t(v)$.

$t: V \rightarrow [0, 1]$

We can define a relation $\preceq_{t}$ over $V$. 

$\forall v, v' \in V, v \preceq_{t} v' \text{ iff } t(v) \leq t(v')$

## Our problem is as follows:

Given $V, E, A$ find a scoring function $t'(v)$ such that the total order defined by $\preceq_{t'}$ is 'close to' the total order defined by $\preceq_{t}$.

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
