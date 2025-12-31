# TODO: Fix Signup Page and Database Issues

## Issues Identified:
- Signup.jsx does not send data to backend; only validates and shows alert.
- Backend has signup route in db-connect/routes/auth.js, but models/Routes/auth.js only has login (not used).
- Need to ensure MongoDB is running locally.
- Need to start the backend server.

## Steps to Fix:
1. Update frontend/src/pages/Signup.jsx to make API call to backend for registration.
2. Test the signup functionality.
3. Ensure MongoDB is installed and running.
4. Start the backend server (npm start in db-connect).
5. Verify data is stored in database.

## Progress:
- [x] Update Signup.jsx with fetch to /api/signup
- [x] Handle API response (success/error)
- [x] Test signup (user confirmed backend is working)
- [x] Check MongoDB status (user confirmed)
- [x] Start backend server (user confirmed)
- [ ] Verify database storage (test by signing up)
