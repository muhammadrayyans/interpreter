user_name = get("Enter name: ")
hidden_key = get("")
status_code = '404'

static_trap = "Warning: {user_name} has invalid {status_code}"
live_view = 'Warning: {user_name} has invalid {status_code}'

display("--- I/O Diagnostics Start ---")

display("1. Literal String Trap (Should NOT replace):")
display(static_trap)

display("2. Formatted String (SHOULD replace):")
display(live_view)

display("3. Direct Variable Display:")
display(status_code)
display(user_name)

combo_alert = 'User {user_name} entered key {hidden_key} at status {status_code}'

display("4. Multi-Variable Interpolation:")
display(combo_alert)

display("--- Diagnostics Complete ---")