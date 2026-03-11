"use client";

// Library page — articles the user has saved/bookmarked

// TODO: Import ArticleCard, Navbar layout components
// TODO: Import api client to call GET /news/library

export default function LibraryPage() {
    // TODO: Fetch saved articles from GET /news/library on mount
    // TODO: State: savedArticles[], isLoading, error

    return (
        <div>
            {/* TODO: <Navbar /> */}
            <main>
                <h1>My Library</h1>
                {/* TODO: Map savedArticles → <ArticleCard /> with unsave action */}
                {/* TODO: Empty state if no saved articles */}
            </main>
        </div>
    );
}
