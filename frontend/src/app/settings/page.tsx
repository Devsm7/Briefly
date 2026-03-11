"use client";

// Settings page — update profile, re-take survey, manage preferences

// TODO: Import Navbar, Input, Button
// TODO: Import useAuth hook for current user data

export default function SettingsPage() {
    // TODO: Load current user from GET /users/me
    // TODO: Form state: fullName
    // TODO: handleSave → PATCH /users/me
    // TODO: Link/button to re-access onboarding survey

    return (
        <div>
            {/* TODO: <Navbar /> */}
            <main>
                <h1>Settings</h1>

                {/* Profile section */}
                {/* TODO: Full name field + save button */}

                {/* Interests section */}
                {/* TODO: "Retake Survey" button → navigate to /onboarding */}
                {/* TODO: Display current preferred categories as badges */}

                {/* Account section */}
                {/* TODO: Change password link (calls reset-password flow) */}
                {/* TODO: Sign out button */}
            </main>
        </div>
    );
}
