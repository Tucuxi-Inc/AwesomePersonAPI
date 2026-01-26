import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from '@/components/common/Layout';
import { ProtectedRoute } from '@/components/common/ProtectedRoute';
import { Login } from '@/pages/Login';
import { Dashboard } from '@/pages/Dashboard';
import { Traits } from '@/pages/Traits';
import { Placeholder } from '@/pages/Placeholder';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route path="/" element={<Dashboard />} />
          <Route path="/candidates" element={<Placeholder title="Candidates" description="Manage job candidates and their assessments" />} />
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
