# Introduction
Description of the project

# Pseudocode
Put pseudocode in this box:

```
Some pseudocode here
```

# Successes


# Struggles
- **Strand directionality complexity**: Implementing the scoring for forward and reverse complement strands required careful thinking through molecular biology principles- that I kept second guessing myself on.

- **Asynchronous collaboration**: Coordinating schedules proved difficult, especially when the group leader was ill for a week. Working asynchronously meant delayed feedback loops and difficulty debugging together in real-time. We had to rely heavily on detailed comments and commit messages to communicate our progress and questions.

- **Unequal workload distribution due to illness**: When one team member is sick, the remaining members must either take on additional work or wait for recovery, both of which impact project momentum and team dynamics.

- **Understanding MCMC conceptually**: Grasping how random sampling can lead to optimal solutions was initially counterintuitive. The probabilistic selection choosing k-mers based on weighted scores rather than always picking the best, which I am not sure led to the correct graph,but we do have a graph


# Personal Reflections
## Group Leader (Nikaela Aitken)
This project was particularly challenging because I was sick for a week during the critical implementation phase, which made staying on top of the concepts and debugging much harder than usual.

To build my understanding of MCMC methods, I relied heavily on video resources:

- [StatQuest: Markov Chain Monte Carlo (MCMC)](https://www.youtube.com/watch?v=7LB1VHp4tLE) - This video helped me understand the fundamental concepts of sampling from distributions and why random walks can find optimal solutions.

- [Gibbs Sampling Explained](https://www.youtube.com/watch?v=MNHIbOqH3sk) - This specifically clarified how Gibbs sampling updates one variable at a time while holding others constant, which is exactly what happens when we exclude one motif and rebuild the PWM.

I also used ChatGPT extensively to discuss MCMC concepts and created the following visualization to understand the acceptance/rejection process:
```mermaid
flowchart TD
    A[Start: Pick an initial point x₀] --> B[For each iteration]
    B --> C[Propose new point x′ = current + random jump]
    C --> D[Compute acceptance ratio: r = target_pdf_x′ / target_pdf_x]
    D --> E{Is r ≥ 1 ?}
    E -- Yes --> F[Accept move: x ← x′]
    E -- No --> G{Is random < r ?}
    G -- Yes --> F[Accept move: x ← x′]
    G -- No --> H[Reject move: stay at current x]
    F --> I[Record x as a sample]
    H --> I[Record x as a sample]
    I --> J{More iterations left?}
    J -- Yes --> C
    J -- No --> K[Done: use all samples to approximate distribution]
```
## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
