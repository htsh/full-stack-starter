import { Link } from "react-router-dom";
import { useAuth } from "@/hooks/use-auth";
import { useCredits } from "@/hooks/use-credits";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const { credits } = useCredits();

  return (
    <div className="mx-auto max-w-4xl p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Button variant="outline" onClick={logout}>
          Sign Out
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Credits</CardTitle>
            <CardDescription>Your current balance</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-4xl font-bold">{credits}</p>
            <Button asChild className="mt-4" size="sm">
              <Link to="/pricing">Buy More</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Profile</CardTitle>
            <CardDescription>Your account details</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">Email</p>
            <p className="font-medium">{user?.email}</p>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <Button asChild size="lg">
          <Link to="/app">Launch AI App</Link>
        </Button>
      </div>
    </div>
  );
}
