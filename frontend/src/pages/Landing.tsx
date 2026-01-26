import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import {
  Brain,
  Target,
  FileText,
  Shield,
  ArrowRight,
  CheckCircle2,
  Sparkles,
} from 'lucide-react';

export default function Landing() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-lg">AP</span>
            </div>
            <div>
              <span className="text-xl font-bold">AP API</span>
              <span className="text-sm text-muted-foreground ml-2">Awesome Person API</span>
            </div>
          </div>
          <Link to="/login">
            <Button size="lg">
              Sign In
              <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-6 py-20 text-center">
        <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-medium mb-6">
          <Sparkles className="h-4 w-4" />
          AI-Powered Talent Assessment
        </div>
        <h1 className="text-5xl font-bold tracking-tight mb-6">
          Hire the Right People with
          <br />
          <span className="text-primary">Evidence-Based Assessment</span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto mb-10">
          The AP API uses the STAR+ methodology and behavioral science to help you
          identify top performers through structured, objective interviews.
        </p>
        <div className="flex items-center justify-center gap-4">
          <Link to="/login">
            <Button size="lg" className="text-lg px-8 py-6">
              Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <Card className="border-2 hover:border-primary/50 transition-colors">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <Brain className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">24 Research-Based Traits</h3>
              <p className="text-muted-foreground">
                Assess candidates across cognitive, interpersonal, execution, and stability dimensions
                with validated behavioral markers.
              </p>
            </CardContent>
          </Card>

          <Card className="border-2 hover:border-primary/50 transition-colors">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <Target className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">STAR+ Methodology</h3>
              <p className="text-muted-foreground">
                Structured interviews with Situation, Task, Action, Result plus reflection
                ensure complete behavioral evidence.
              </p>
            </CardContent>
          </Card>

          <Card className="border-2 hover:border-primary/50 transition-colors">
            <CardContent className="p-6">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Complete Traceability</h3>
              <p className="text-muted-foreground">
                Every score links to specific evidence. Understand exactly why candidates
                received their assessment.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-white py-16">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {[
              { step: '1', title: 'Add Candidates', desc: 'Import candidates and their resumes' },
              { step: '2', title: 'Select Traits', desc: 'Choose which traits to assess for the role' },
              { step: '3', title: 'Conduct Interview', desc: 'AI-guided behavioral interview with probes' },
              { step: '4', title: 'Get Results', desc: 'Receive calibrated scores with full evidence' },
            ].map((item) => (
              <div key={item.step} className="text-center">
                <div className="w-12 h-12 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="font-semibold mb-2">{item.title}</h3>
                <p className="text-sm text-muted-foreground">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div>
            <h2 className="text-3xl font-bold mb-6">Why AP API?</h2>
            <ul className="space-y-4">
              {[
                'Objective, evidence-based hiring decisions',
                'Reduce unconscious bias with structured interviews',
                'Identify counter-indicators that predict failure',
                'Build organization-specific rubrics from top performers',
                'Complete audit trails for compliance',
              ].map((benefit) => (
                <li key={benefit} className="flex items-start gap-3">
                  <CheckCircle2 className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <span>{benefit}</span>
                </li>
              ))}
            </ul>
          </div>
          <Card className="bg-slate-900 text-white">
            <CardContent className="p-8">
              <Shield className="h-12 w-12 text-primary mb-4" />
              <h3 className="text-xl font-semibold mb-3">Built for Compliance</h3>
              <p className="text-slate-300 mb-4">
                Designed with employment law in mind. Document job-relatedness,
                monitor for disparate impact, and maintain complete audit trails.
              </p>
              <div className="text-sm text-slate-400">
                Supports NYC Local Law 144, EEOC Guidelines, GDPR Article 22
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-primary text-primary-foreground py-16">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Hiring?</h2>
          <p className="text-lg opacity-90 mb-8">
            Start conducting evidence-based interviews today.
          </p>
          <Link to="/login">
            <Button size="lg" variant="secondary" className="text-lg px-8 py-6">
              Sign In to Get Started
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-8">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-8 h-8 bg-primary rounded flex items-center justify-center">
              <span className="text-primary-foreground font-bold text-sm">AP</span>
            </div>
            <span className="text-white font-semibold">AP API</span>
          </div>
          <p className="text-sm">
            &copy; 2026 Tucuxi Inc. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
