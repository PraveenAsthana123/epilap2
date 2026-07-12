# Evaluation Rigor — DCA · Bootstrap CIs · DeLong · Nested CV

> **Why (this doc):** Point estimates are not enough for a defensible model; this adds clinical
> net-benefit, uncertainty on the metric, a formal model-comparison test, and unbiased nested
> performance. **How:** `analysis/evaluation.py`.

## ROC-AUC with bootstrap 95% CIs
*Caption - AUC with 1000-sample bootstrap confidence intervals — the metric's uncertainty, not just a point.*

| model | auc | ci95 |
|---|---|---|
| LogReg | 0.928 | [0.885, 0.962] |
| RandomForest | 0.931 | [0.887, 0.963] |

## Model comparison — DeLong test
AUC(LogReg) = 0.927 vs AUC(RF) = 0.93; **DeLong p = 0.797**
(no significant difference at α=0.05).

## Decision Curve Analysis (clinical net benefit)
![DCA](analysis/outputs/evaluation/dca.png)

The model curve above *treat-all* and *treat-none* across the plausible threshold range means it
adds net clinical benefit (fewer unnecessary actions than treating everyone).

## Nested cross-validation (unbiased, inner HPO)
Nested CV ROC-AUC = **0.934 ± 0.024** (5 outer × 3 inner folds; inner grid over
`n_estimators` × `max_depth`) — removes the optimistic bias of tuning and testing on the same folds.

**Reason:** Evaluate models the way a top journal / doctoral panel expects. **Why:** CIs, formal comparison, net benefit, and nested CV are table-stakes for rigour. **What is happening:** AUC uncertainty is quantified; models are compared formally; clinical utility is shown. **How it is happening:** Bootstrap CIs, DeLong test, DCA, and nested CV are computed from the data. **Reference:** DeLong et al. (1988); Vickers & Elkin (2006); Cawley & Talbot (2010).

## References

Cawley, G. C., & Talbot, N. L. C. (2010). On over-fitting in model selection and subsequent selection bias. *JMLR, 11*, 2079-2107.

DeLong, E. R., DeLong, D. M., & Clarke-Pearson, D. L. (1988). Comparing the areas under two or more correlated ROC curves. *Biometrics, 44*(3), 837-845.

Vickers, A. J., & Elkin, E. B. (2006). Decision curve analysis. *Medical Decision Making, 26*(6), 565-574.
