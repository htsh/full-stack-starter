import { useState } from "react";
import { Link } from "react-router-dom";
import api from "@/lib/api";
import { useAuthStore } from "@/stores/auth-store";
import { useCredits } from "@/hooks/use-credits";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function AppPage() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const { credits } = useCredits();
  const setUser = useAuthStore((s) => s.setUser);

  async function handleGenerate(e: React.FormEvent) {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true);
    setResult("");

    try {
      const { data } = await api.post("/ai/generate", { prompt });
      setResult(data.result);
      // Update credits in store
      const meRes = await api.get("/users/me");
      setUser(meRes.data);
    } catch (err: unknown) {
      const detail =
        err && typeof err === "object" && "response" in err
          ? (err as { response?: { data?: { detail?: string } } }).response
              ?.data?.detail
          : undefined;
      setResult(detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">AI Playground</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-muted-foreground">
            {credits} credits
          </span>
          <Button asChild variant="outline" size="sm">
            <Link to="/dashboard">Back</Link>
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Generate</CardTitle>
          <CardDescription>
            Each request costs 1 credit
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleGenerate} className="grid gap-4">
            <Input
              placeholder="Enter your prompt..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
            />
            <Button type="submit" disabled={loading || credits < 1}>
              {loading ? "Generating..." : "Generate"}
            </Button>
          </form>

          {result && (
            <div className="mt-6 rounded-md bg-muted p-4">
              <p className="whitespace-pre-wrap">{result}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
