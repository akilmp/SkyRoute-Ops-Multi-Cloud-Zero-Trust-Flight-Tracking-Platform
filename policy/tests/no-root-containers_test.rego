package no_root_containers_test

import data.norootcontainers

bad_pod := {
  "kind": "Pod",
  "spec": {
    "containers": [{"name": "app", "image": "nginx"}]
  }
}

good_pod := {
  "kind": "Pod",
  "spec": {
    "containers": [{"name": "app", "image": "nginx", "securityContext": {"runAsNonRoot": true}}]
  }
}

test_container_without_security_context_is_denied if {
  violations := norootcontainers.violation with input as {"review": {"kind": {"kind": "Pod"}, "object": bad_pod}}
  count(violations) == 1
}

test_container_with_run_as_non_root_is_allowed if {
  violations := norootcontainers.violation with input as {"review": {"kind": {"kind": "Pod"}, "object": good_pod}}
  count(violations) == 0
}
