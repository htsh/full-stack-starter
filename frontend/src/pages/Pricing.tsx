import { useState } from "react";
import { Link } from "react-router-dom";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

const packages = [
  { id: "starter", name: "Starter Pack", credits: 50, price: "$4.99" },
  { id: "pro", name: "Pro Pack", credits: 200, price: "$14.99" },
  { id: "mega", name: "Mega Pack", credits: 500, price: "$29.99" },
];

export default function Pricing() {
  const [loading, setLoading] = useState<string | null>(null);

  async function handleCheckout(packageId: string) {
    setLoading(packageId);
    try {
      const { data } = await api.post("/payments/checkout", {
        package_id: packageId,
      });
      window.location.href = data.checkout_url;
    } catch {
      alert("Failed to start checkout");
      setLoading(null);
    }
  }

  return (
    <div className="mx-auto max-w-4xl p-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Buy Credits</h1>
        <Button asChild variant="outline">
          <Link to="/dashboard">Back</Link>
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {packages.map((pkg) => (
          <Card key={pkg.id}>
            <CardHeader>
              <CardTitle>{pkg.name}</CardTitle>
              <CardDescription>{pkg.credits} credits</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="mb-4 text-3xl font-bold">{pkg.price}</p>
              <Button
                className="w-full"
                onClick={() => handleCheckout(pkg.id)}
                disabled={loading === pkg.id}
              >
                {loading === pkg.id ? "Redirecting..." : "Buy Now"}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
