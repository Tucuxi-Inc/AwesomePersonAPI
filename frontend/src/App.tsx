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
import { Compliance } from '@/pages/Compliance';
import TopPerformers from '@/pages/TopPerformers';
import ProfilingSession from '@/pages/ProfilingSession';
import RoleTemplates from '@/pages/RoleTemplates';
import InvitationLanding from '@/pages/InvitationLanding';
import Rubrics from '@/pages/Rubrics';
import Settings from '@/pages/Settings';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/invite/:token" element={<InvitationLanding />} />

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
          <Route path="/roles" element={<RoleTemplates />} />
          <Route path="/roles/:roleId" element={<Placeholder title="Role Profile" description="View and edit role profile details" />} />
          <Route path="/traits" element={<Traits />} />
          <Route path="/rubrics" element={<Rubrics />} />
          <Route path="/profiling" element={<TopPerformers />} />
          <Route path="/profiling/:sessionId" element={<ProfilingSession />} />
          <Route path="/compliance" element={<Compliance />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
