# Import API Design Overview

## Functional Requirements

1. **Import Question Logs from Coding Platforms**
   - Users can import their question logs from supported coding platforms (e.g., Codewars, LeetCode, HackerRank).
   - The API endpoint is `/import/{platform}/`, where `{platform}` is the name of the coding platform.

2. **User Profile Submission**
   - The user must provide a profile payload (typically a username) in the POST request body.
   - The API validates the presence and correctness of this payload.

3. **Platform-Specific Handling**
   - The API can handle different platforms, each potentially having unique requirements or error codes.
   - The system is designed to be extensible for additional platforms.

4. **Data Mapping**
   - Imported data is mapped into the system’s internal question log format.
   - The API ensures that the imported data is correctly stored and retrievable.

5. **Error Handling**
   - The API must handle and report errors from upstream platforms (e.g., timeouts, not found, server errors).
   - The API returns appropriate HTTP status codes (e.g., 400 for bad input, 500 for upstream errors).

---

## Non-Functional Requirements

1. **Extensibility**
   - The design allows for easy addition of new platforms with minimal changes.

2. **Robustness**
   - The API must gracefully handle invalid input and upstream errors.
   - Tests ensure that the API does not break when platforms are unavailable or return errors.

3. **Testability**
   - The API is covered by integration tests that simulate various scenarios, including success, invalid input, and upstream errors.

4. **Security**
   - Only valid, authenticated requests should be processed (not shown in the test, but implied for production).

---

## User Flow

1. **User Action**
   - The user initiates an import by sending a POST request to `/import/{platform}/` with their username (or other required profile info).

2. **API Processing**
   - The API receives the request, validates the input, and attempts to fetch/import data from the specified platform.
   - If the input is invalid, the API returns a 400 error.
   - If the platform returns an error, the API returns a 500 error (or other appropriate code).

3. **Data Mapping**
   - If the import is successful, the API maps the imported data into the internal question log format and stores it.

4. **Feedback**
   - The user receives a response indicating success or failure.
   - On success, the imported logs are available via the system’s question log endpoints.

---

## Example User Experience

- The user visits an "Import" page in the UI, selects "Codewars," enters their username, and clicks "Import."
- The frontend sends a POST request to `/import/codewars/` with the username.
- The backend fetches the user’s data from Codewars, maps it, and stores it.
- The user is notified of success, and the new logs appear in their activity list.
- If there’s an error (e.g., wrong username, Codewars is down), the user sees an error message.

---

**Summary:**
The import API is designed to let users easily bring in their coding activity from various platforms, with robust validation, error handling, and extensibility for future platforms. The flow is simple and user-centric, focusing on a smooth import experience.

## Implementation Notes

The `/import/<platform>/` endpoint is provided by `ImportAPIView`. The view
validates a `username` field and then enqueues an asynchronous task by
publishing a message to an AWS SQS queue. Tasks are defined in
`backend/infrastructure/tasks.py` and executed by a Lambda function (see
`infra/lambda/handler.py`). The queue URL is configured via the
`IMPORT_QUEUE_URL` setting so local development can skip SQS and run tasks
synchronously when the variable is unset.

Background tasks fetch data from the target platform (initially Codewars) and
create `Question` and `QuestionLog` records. The worker includes basic rate
limiting with a short `sleep()` call and logs any errors returned from the
remote API so they surface in the Lambda logs.
