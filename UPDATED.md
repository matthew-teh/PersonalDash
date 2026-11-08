# This markdown serves as a preparation for terra hackclub devlogging.
# for real real markdown please see README.md

V2.1 - Logged

Added Light and Dark Theme

V2.2

Added - Logged
- A world clock card
- Sidebar for adding widgets.
- Animated Reload Button ( Top right reload button of webpage only. )
- Animated cards appearing
- Cards per row are adjustable in setting.

V2.3 - Logged

Added 
- Animated Reload Button for all widgets # Cancelled
- Completed world clock card

V2.4 - Logged

Rewrote structure
- crypto.py, weather.py, worldclock.py for clean code and precise alignment of cards. # weather left

V2.5 - Logged
- Introducing Weather and World clock cards settings autocomplete.
- Added setting : Border smoothness, dark light mode colors 
- Dark light mode fully compatible with all components
- Add cards sidebar now have compatibility to dark, light mode.

V2.6 - Shipped

- Add card: Pomodoro timer
- Terra Theme Special Edition : Tic Tac Toe

V3 - Logged
- A complete login system with security-
- Session persistance 
- Rate limit of login works.

V3.1 - Logged
- Migrating localstroage to sqlite3, enable multi device ( desktop/laptop web only. )

V3.2 - Logged
- Optimizing sqlite3 from disk read to redis server, ram only. Periodically save to disk.
- Now cloud syncting
- New card: Quick Notes, support syncing between devices.

V3.3 Update - Logged

I added a delete account button
Confirmation on sign out
Separate auth.py to prevent two work in one file. Now database.py and auth.py

V3.4 Update - Logged
- I optimized code structure
- I added forget password in signin page, you can reset password incase you forget.
- Recovery code added to help reseting password.

V3.5 Update - Shipped
- Optimized image icons file placement
- Added new card: Terra Countdown, it can remind you how much time left to next week.
- Moved tutorial how to run to RUNNING.md
- Added 'device logged in' in user info button.

V4 - Planned
- Optimize state.py ( it is too much code with many garbage, trying to use variables as useful as possible. )


# Delayed
- Phone compatibility

