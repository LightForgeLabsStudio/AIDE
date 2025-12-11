# GUT Assertion Reference - v9.5.1

**Quick reference for available assert methods in GUT (Godot Unit Test) framework.**

Source: [GUT ReadTheDocs - GutTest Class Reference](https://gut.readthedocs.io/en/latest/class_ref/class_guttest.html)

## Comparison Assertions

- `assert_eq(got, expected, text = "")` - Asserts expected equals got
- `assert_ne(got, not_expected, text = "")` - Asserts inequality
- `assert_almost_eq(got, expected, error_interval, text = "")` - Value within range
- `assert_almost_ne(got, not_expected, error_interval, text = "")` - Value outside range
- `assert_eq_deep(v1, v2)` - Deep comparison of arrays/dictionaries
- `assert_ne_deep(v1, v2)` - Deep inequality comparison
- `assert_same(v1, v2, text = "")` - Verifies identity (is_same)
- `assert_not_same(v1, v2, text = "")` - Verifies not identical

## Numeric Assertions

- `assert_gt(got, expected, text = "")` - Greater than
- `assert_gte(got, expected, text = "")` - Greater than or equal
- `assert_lt(got, expected, text = "")` - Less than
- `assert_lte(got, expected, text = "")` - Less than or equal
- `assert_between(got, expect_low, expect_high, text = "")` - Inclusive range check
- `assert_not_between(got, expect_low, expect_high, text = "")` - Outside range

## Boolean Assertions

- `assert_true(got, text = "")` - Asserts boolean true (not truthiness)
- `assert_false(got, text = "")` - Asserts boolean false (not falsiness)

## Null/Existence Assertions

- `assert_null(got, text = "")` - Value is null
- `assert_not_null(got, text = "")` - Value is not null

## Type Assertions

- `assert_is(object, a_class, text = "")` - Object extends class
- `assert_typeof(object, type, text = "")` - Matches TYPE_* constant
- `assert_not_typeof(object, type, text = "")` - Doesn't match TYPE_*

## Collection Assertions

- `assert_has(obj, element, text = "")` - Uses obj.has() to check for element
- `assert_does_not_have(obj, element, text = "")` - Validates no element

## String Assertions

- `assert_string_contains(text, search, match_case = true)` - Contains substring
- `assert_string_starts_with(text, search, match_case = true)` - Starts with substring
- `assert_string_ends_with(text, search, match_case = true)` - Ends with substring

## File Assertions

- `assert_file_exists(file_path)` - File exists
- `assert_file_does_not_exist(file_path)` - File doesn't exist
- `assert_file_empty(file_path)` - File is empty
- `assert_file_not_empty(file_path)` - File has content

## Object/Property Assertions

- `assert_has_method(obj, method, text = "")` - Object has method
- `assert_has_signal(object, signal_name, text = "")` - Object has signal
- `assert_exports(obj, property_name, type)` - Exports property with type
- `assert_property(obj, property_name, default_value, new_value)` - Getter/setter test
- `assert_property_with_backing_variable(obj, property_name, default_value, new_value, backed_by_name = null)` - Test with backing variable
- `assert_accessors(obj, property, default, set_to)` - Test public get/set methods

## Signal Assertions

- `assert_signal_emitted(p1, p2 = "", p3 = "")` - Signal was emitted
- `assert_signal_not_emitted(p1, p2 = "", p3 = "")` - Signal not emitted
- `assert_signal_emitted_with_parameters(p1, p2, p3 = -1, p4 = -1)` - Signal with params
- `assert_signal_emit_count(p1, p2, p3 = 0, p4 = "")` - Signal fired N times

## Connection Assertions

- `assert_connected(p1, p2, p3 = null, p4 = "")` - Signal connected
- `assert_not_connected(p1, p2, p3 = null, p4 = "")` - Signal not connected

## Double/Mock Assertions

- `assert_called(inst, method_name = null, parameters = null)` - Method called on doubled class
- `assert_not_called(inst, method_name = null, parameters = null)` - Method not called
- `assert_called_count(callable, expected_count)` - Method called N times

## Memory Assertions

- `assert_freed(obj, title = "something")` - Object has been freed
- `assert_not_freed(obj, title = "something")` - Object not freed
- `assert_no_new_orphans(text = "")` - No orphaned nodes created

## Error Tracking Assertions

- `assert_engine_error(text, msg = "")` - Engine error with text occurred
- `assert_engine_error_count(count, msg = "")` - N engine errors occurred
- `assert_push_error(text, msg = "")` - push_error with text occurred
- `assert_push_error_count(count, msg = "")` - N push_error calls
- `assert_push_warning(text, msg = "")` - push_warning with text occurred
- `assert_push_warning_count(count, msg = "")` - N push_warning calls

---

## Common Patterns

### Testing Numeric Ranges
```gdscript
assert_gte(value, 0, "Should be non-negative")
assert_lte(value, 100, "Should be at most 100")
assert_between(value, 0, 100, "Should be 0-100")
```

### Testing Collections
```gdscript
assert_has(dictionary, "key", "Should have key")
assert_eq_deep(array1, array2)  # Deep comparison
```

### Testing Signals
```gdscript
watch_signals(object)
object.do_something()
assert_signal_emitted(object, "something_happened")
assert_signal_emitted_with_parameters(object, "data_changed", ["value"])
```

### Testing Types
```gdscript
assert_is(instance, MyClass, "Should be instance of MyClass")
assert_typeof(value, TYPE_DICTIONARY, "Should be dictionary")
```
