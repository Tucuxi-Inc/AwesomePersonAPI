import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/common/Layout';
import { ProtectedRoute } from '@/components/common/ProtectedRoute';
import { Login } from '@/pages/Login';
import { Dashboard } from '@/pages/Dashboard';
import { Traits } from '@/pages/Traits';
import { Placeholder } from '@/pages/Placeholder';
import Landing from '@/pages/Landing';
import Candidates from '@/pages/Candidates';
import StartInterview from '@/pages/StartInterview';
import Interviews from '@/pages/Interviews';
import Interview from '@/pages/Interview';
import AssessmentResults from '@/pages/AssessmentResults';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />

        {/* Protected routes */}
        <Route
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/candidates" element={<Candidates />} />
          <Route path="/candidates/:candidateId/start-interview" element={<StartInterview />} />
          <Route path="/interviews" element={<Interviews />} />
          <Route path="/interviews/:sessionId" element={<Interview />} />
          <Route path="/interviews/:sessionId/results" element={<AssessmentResults />} />
          <Route path="/roles" element={<Placeholder title="Role Profiles" description="Configure role requirements and trait mappings" />} />
          <Route path="/traits" element={<Traits />} />
          <Route path="/rubrics" element={<Placeholder title="Scoring Rubrics" description="View and customize assessment rubrics" />} />
          <Route path="/settings" element={<Placeholder title="Settings" description="Configure your organization and preferences" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
