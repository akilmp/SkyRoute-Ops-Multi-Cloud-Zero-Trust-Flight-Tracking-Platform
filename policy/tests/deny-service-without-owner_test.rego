package deny_service_without_owner_test

import data.denyservicewithoutowner

test_service_missing_owner_is_denied if {
  svc := {"kind": "Service", "metadata": {"name": "svc"}}
  violations := denyservicewithoutowner.violation with input as {"review": {"kind": {"kind": "Service"}, "object": svc}}
  count(violations) == 1
}

test_service_with_owner_is_allowed if {
  svc := {"kind": "Service", "metadata": {"name": "svc", "labels": {"owner": "team"}}}
  violations := denyservicewithoutowner.violation with input as {"review": {"kind": {"kind": "Service"}, "object": svc}}
  count(violations) == 0
}
