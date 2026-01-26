import { useEffect, useState } from 'react';
import { api } from '@/api/client';
import { Trait } from '@/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

interface TraitCategory {
  name: string;
  traits: Trait[];
}

const categoryLabels: Record<string, string> = {
  COGNITIVE: 'Cognitive Traits',
  INTERPERSONAL: 'Interpersonal Traits',
  EXECUTION: 'Execution Traits',
  STABILITY: 'Stability Traits',
  SELF_MANAGEMENT: 'Self-Management Traits',
  ORIENTATION: 'Orientation Traits',
};

export function Traits() {
  const [categories, setCategories] = useState<TraitCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTrait, setSelectedTrait] = useState<Trait | null>(null);

  useEffect(() => {
    const fetchTraits = async () => {
      try {
        const response = await api.getTraitCategories();
        setCategories(response.data);
      } catch (error) {
        console.error('Failed to fetch traits:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTraits();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Trait Taxonomy</h1>
        <p className="text-muted-foreground mt-1">
          24 traits organized into 6 categories with role-context valence mappings.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Trait list by category */}
        <div className="space-y-6">
          {categories.map((category) => (
            <Card key={category.name}>
              <CardHeader>
                <CardTitle>{categoryLabels[category.name] || category.name}</CardTitle>
                <CardDescription>{category.traits.length} traits</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {category.traits.map((trait) => (
                    <button
                      key={trait.id}
                      onClick={() => setSelectedTrait(trait)}
                      className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                        selectedTrait?.id === trait.id
                          ? 'bg-primary text-primary-foreground'
                          : 'hover:bg-accent'
                      }`}
                    >
                      {trait.name}
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Trait detail */}
        <div className="lg:sticky lg:top-8">
          {selectedTrait ? (
            <Card>
              <CardHeader>
                <CardTitle>{selectedTrait.name}</CardTitle>
                <CardDescription>{selectedTrait.category}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="font-medium mb-1">Definition</h4>
                  <p className="text-sm text-muted-foreground">{selectedTrait.definition}</p>
                </div>

                <div>
                  <h4 className="font-medium mb-2">Spectrum</h4>
                  <div className="flex items-center text-sm">
                    <span className="text-muted-foreground">{selectedTrait.spectrum_low_label}</span>
                    <div className="flex-1 mx-4 h-2 bg-muted rounded-full">
                      <div className="h-full w-1/2 bg-primary rounded-full"></div>
                    </div>
                    <span className="text-muted-foreground">{selectedTrait.spectrum_high_label}</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium mb-2">Low Markers</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {selectedTrait.behavioral_markers_low.map((marker, i) => (
                        <li key={i}>• {marker}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">High Markers</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {selectedTrait.behavioral_markers_high.map((marker, i) => (
                        <li key={i}>• {marker}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {selectedTrait.counter_indicator_for.length > 0 && (
                  <div>
                    <h4 className="font-medium mb-2 text-destructive">Counter-Indicator For</h4>
                    <ul className="text-sm text-muted-foreground space-y-1">
                      {selectedTrait.counter_indicator_for.map((role, i) => (
                        <li key={i}>• {role}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="flex items-center justify-center h-64 text-muted-foreground">
                Select a trait to view details
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
