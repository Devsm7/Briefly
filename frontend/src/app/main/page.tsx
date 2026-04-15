"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ThumbsUp, ThumbsDown, LogOut, TrendingUp } from "lucide-react";
import { toast } from "sonner";

type Interest = "tech" | "politics" | "business" | "sport";

interface Article {
  id: string;
  title: string;
  summary: string;
  category: Interest;
  source: string;
  publishedAt: string;
  liked?: boolean;
  disliked?: boolean;
}

const mockArticles: Article[] = [
  {
    id: "1",
    title: "New AI Model Breaks Performance Records in Natural Language Processing",
    summary: "Researchers have unveiled a groundbreaking AI model that achieves unprecedented accuracy in understanding context and generating human-like responses. The model demonstrates significant improvements in multilingual capabilities and reduced computational requirements.",
    category: "tech",
    source: "Tech Innovation Daily",
    publishedAt: "2026-04-02T08:30:00Z",
  },
  {
    id: "2",
    title: "Global Climate Summit Reaches Historic Agreement on Carbon Emissions",
    summary: "World leaders have signed a comprehensive agreement committing to aggressive carbon reduction targets. The accord includes binding commitments from major economies and establishes new funding mechanisms for renewable energy development in emerging nations.",
    category: "politics",
    source: "Global Politics Review",
    publishedAt: "2026-04-02T07:15:00Z",
  },
  {
    id: "3",
    title: "Tech Giants Report Record Quarterly Earnings Amid Market Volatility",
    summary: "Leading technology companies have posted exceptional quarterly results, defying market uncertainties. Cloud computing and AI services drove significant revenue growth, with several firms exceeding analyst expectations by considerable margins.",
    category: "business",
    source: "Financial Times Today",
    publishedAt: "2026-04-02T09:00:00Z",
  },
  {
    id: "4",
    title: "Olympic Champion Announces Comeback After Two-Year Break",
    summary: "The decorated athlete confirmed plans to return to competitive sports following an extended hiatus. Training has resumed with a focus on the upcoming international championships, where the champion aims to reclaim the title.",
    category: "sport",
    source: "Sports World News",
    publishedAt: "2026-04-02T06:45:00Z",
  },
  {
    id: "5",
    title: "Quantum Computing Breakthrough Promises Revolutionary Applications",
    summary: "Scientists have achieved a major milestone in quantum computing stability, maintaining quantum states for record durations. This advancement could accelerate the development of practical quantum computers for solving complex real-world problems.",
    category: "tech",
    source: "Science & Technology Weekly",
    publishedAt: "2026-04-01T14:20:00Z",
  },
  {
    id: "6",
    title: "Election Results Trigger Major Political Realignment",
    summary: "Recent elections have produced unexpected outcomes, leading to significant shifts in legislative power. Political analysts predict transformative policy changes across multiple sectors including healthcare, education, and infrastructure.",
    category: "politics",
    source: "Political Insights",
    publishedAt: "2026-04-01T20:30:00Z",
  },
  {
    id: "7",
    title: "Startup Unicorn Raises Billion-Dollar Funding Round",
    summary: "A rapidly growing startup has secured massive investment from leading venture capital firms, reaching unicorn status. The company plans to expand internationally and accelerate product development in sustainable technology solutions.",
    category: "business",
    source: "Startup Business Journal",
    publishedAt: "2026-04-01T11:00:00Z",
  },
  {
    id: "8",
    title: "Championship Finals Draw Record-Breaking Viewership Numbers",
    summary: "The highly anticipated finals captivated audiences worldwide, setting new viewership records across streaming and traditional broadcast platforms. The thrilling competition featured remarkable performances and dramatic moments throughout.",
    category: "sport",
    source: "Sports Broadcasting Network",
    publishedAt: "2026-04-01T19:45:00Z",
  },
];

export default function Main() {
  const router = useRouter();
  const [articles, setArticles] = useState<Article[]>([]);
  const [userInterests, setUserInterests] = useState<Record<Interest, number>>({} as Record<Interest, number>);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedInterests = localStorage.getItem("userInterests");
    if (!storedInterests) {
      router.push("/survey");
      return;
    }

    const interests = JSON.parse(storedInterests) as Record<Interest, number>;
    setUserInterests(interests);

    setTimeout(() => {
      const recommendedArticles = mockArticles
        .map((article) => ({
          ...article,
          relevanceScore: interests[article.category] || 0,
        }))
        .sort((a, b) => b.relevanceScore - a.relevanceScore);

      setArticles(recommendedArticles);
      setLoading(false);
    }, 1000);
  }, [router]);

  const handleLike = (articleId: string) => {
    setArticles((prev) =>
      prev.map((article) =>
        article.id === articleId
          ? { ...article, liked: !article.liked, disliked: false }
          : article
      )
    );
    toast.success("Thanks for your feedback! We'll show you more content like this.");
  };

  const handleDislike = (articleId: string) => {
    setArticles((prev) =>
      prev.map((article) =>
        article.id === articleId
          ? { ...article, disliked: !article.disliked, liked: false }
          : article
      )
    );
    toast.success("Thanks for your feedback! We'll show you less content like this.");
  };

  const handleLogout = () => {
    localStorage.removeItem("userInterests");
    localStorage.removeItem("userEmail");
    router.push("/");
  };

  const getCategoryColor = (category: Interest) => {
    const colors = {
      tech: "bg-blue-100 text-blue-800",
      politics: "bg-red-100 text-red-800",
      business: "bg-green-100 text-green-800",
      sport: "bg-orange-100 text-orange-800",
    };
    return colors[category];
  };

  const getCategoryLabel = (category: Interest) => {
    return category.charAt(0).toUpperCase() + category.slice(1);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));

    if (diffHours < 1) return "Just now";
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${Math.floor(diffHours / 24)}d ago`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
        <div className="text-center">
          <TrendingUp className="w-12 h-12 mx-auto mb-4 animate-pulse text-blue-600" />
          <p className="text-lg text-gray-600">Analyzing your interests...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Your News Feed</h1>
            <p className="text-sm text-gray-600">
              Personalized recommendations based on your interests
            </p>
          </div>
          <Button variant="outline" onClick={handleLogout}>
            <LogOut className="w-4 h-4 mr-2" />
            Logout
          </Button>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="mb-6 flex gap-2 flex-wrap">
          {Object.entries(userInterests)
            .sort(([, a], [, b]) => b - a)
            .map(([interest, score]) => (
              <Badge key={interest} variant="secondary" className="text-sm">
                {getCategoryLabel(interest as Interest)} ({score})
              </Badge>
            ))}
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          {articles.map((article) => (
            <Card key={article.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <Badge className={getCategoryColor(article.category)}>
                    {getCategoryLabel(article.category)}
                  </Badge>
                  <span className="text-xs text-gray-500">
                    {formatDate(article.publishedAt)}
                  </span>
                </div>
                <CardTitle className="text-xl">{article.title}</CardTitle>
                <CardDescription className="text-xs text-gray-500">
                  {article.source}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-700 mb-4">{article.summary}</p>
                <div className="flex items-center gap-2">
                  <Button
                    variant={article.liked ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleLike(article.id)}
                  >
                    <ThumbsUp className="w-4 h-4 mr-1" />
                    Like
                  </Button>
                  <Button
                    variant={article.disliked ? "default" : "outline"}
                    size="sm"
                    onClick={() => handleDislike(article.id)}
                  >
                    <ThumbsDown className="w-4 h-4 mr-1" />
                    Dislike
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
}
