import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

export default function Landing() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-8 p-8">
      <h1 className="text-5xl font-bold tracking-tight">AI App</h1>
      <p className="max-w-md text-center text-lg text-muted-foreground">
        Powerful AI features at your fingertips. Sign up, buy credits, and start
        creating.
      </p>
      <div className="flex gap-4">
        <Button asChild size="lg">
          <Link to="/register">Get Started</Link>
        </Button>
        <Button asChild variant="outline" size="lg">
          <Link to="/login">Sign In</Link>
        </Button>
      </div>
    </div>
  );
}
