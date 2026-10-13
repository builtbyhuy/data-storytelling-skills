# Use $1,200 as invoiced revenue

The $2,500 total contains **$1,300 of repeated invoice amounts**. The payment join did not create revenue.

INV-1001 has two payment allocations, so its $300 invoice appears twice. INV-1002 has three allocations, so its $500 invoice appears three times. Together, those extra copies add $1,300. The unpaid $150 invoice remains in the left join; switching to an inner join would remove it while leaving the duplication.

Aggregate invoice lines and payment allocations separately by invoice ID, then join the two invoice-level summaries. The result is **$1,200 invoiced, $1,050 received, and $150 outstanding** across four invoices. Preserve every legitimate service line and payment allocation.

The many-to-many relationship is valid for these exports. It does not make the resulting revenue sum valid. Use the original invoice-line total for revenue and the allocation total for collections; reconcile at their shared invoice grain.
