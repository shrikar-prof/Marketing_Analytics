# Agent dialogue log

Questions sent by the growth-strategy-partner to the ml-statistician by direct agent message, verbatim as reported by the partner, with the memo section each affected and what changed. The statistician's answers, with method, are in `reports/ml_followups.md` (Round 1 Q1 to Q6, Round 2 Q1 to Q3). Two rounds; the fallback relay was not used.

## Round 1

1. (Memo s.5 Pilot 2, autopay) Month-to-month fiber customers split by payment method (electronic check / mailed check / bank transfer auto / credit card auto): count, churn rate, mean monthly bill.
   - Section affected: s.1 lever 3, s.3.1 and Pilot 3. The autopay pilot ended up as Pilot 3, not Pilot 2 as the question said.
   - What changed: it confirmed a big gap (60.4% for electronic check vs 41.6–45.6% for autopay), which is why the autopay pilot exists.

2. (Memo s.3, contract selection check) Churn rate and count for one-year and two-year contract customers with tenure 0-12 months, split fiber vs DSL.
   - Section affected: none.
   - What changed: nothing. The only groups were 7 to 42 customers, too few to read, so the memo does not use the answer and the selection caveat stays unquantified.

3. (Memo s.5 Pilot 3, fiber onboarding/support) Month-to-month fiber customers with vs without TechSupport: count, churn rate, mean monthly bill.
   - Section affected: s.3.1 and Pilot 4. The question said Pilot 3.
   - What changed: it gave Pilot 4's trigger (57.5% vs 38.9%) and its 1,796-customer test group.

4. (Memo s.3 targeting) Within the top 1,060 contract-lever customers (smallest_intervention_profile): share paying by electronic check, share without TechSupport, share SeniorCitizen.
   - Section affected: Pilot 4.
   - What changed: only the 87.2% without tech support was used, to back Pilot 4. The 61.7% electronic-check share and 25.5% senior share were not used.

5. (Memo s.3 threshold economics) Held-out test at cutoffs 0.30, 0.40, 0.50, 0.60: customers flagged, true leavers flagged, summed monthly bill of flagged leavers, summed monthly bill of flagged stayers.
   - Section affected: s.3.3.
   - What changed: these counts built the threshold table, the break-even save rates and the recommended cutoff of 0.4 to 0.5.

6. (Memo s.3 fairness guardrail) SeniorCitizen share in the pooled top-20% risk group vs the whole base.
   - Section affected: s.3.2, Track A item 7 and Pilot 1 guardrails.
   - What changed: it added the "senior share within 5 points" guardrail, because seniors are 30.7% of the top-risk group vs 16.2% of the base.

## Round 2

1. (Memo s.5 Pilot 2 sizing) Month-to-month fiber, tenure 0-12 (the 916): split electronic check / mailed check / automatic (bank+card): customers, churn rate, mean bill.
   - Section affected: s.1 lever 3, s.3.1 and Pilot 3. The question said Pilot 2.
   - What changed: autopay payers in their first year leave as often as electronic-check payers (72.2% vs 71.2%). So the autopay lever was retargeted to customers past month 12: 676 customers, 50.3% vs 33.6% churn, which I worked out from the counts.

2. (Memo s.5 Pilot 3 onboarding) Month-to-month fiber churn by tenure band 0-2, 3-6, 7-12 months: customers, churn rate.
   - Section affected: s.1 thesis, s.1.1, s.3.1, Pilot 2 and lever 2. The question said Pilot 3.
   - What changed: the 80.5% churn in months 0–2 became the core of the thesis and Pilot 2's trigger. It is also the basis of the assumed intake of about 115 new customers a month.

3. (Memo s.3/s.5 Pilot 1 targeting) Month-to-month customers by pooled score band <0.3, 0.3-0.5, 0.5-0.7, >=0.7: customers, actual churn rate, mean bill.
   - Section affected: s.1 lever 1, s.3.1 and Pilot 1.
   - What changed: Pilot 1's target group became the 2,548 customers scored 0.3 or higher (55.3% churn, $76.41 mean bill), split randomly within each score band. This also set the $96k–$203k sizing for lever 1.
