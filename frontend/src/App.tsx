import { Routes, Route } from 'react-router-dom';
import { EngineeringTeamPage } from './pages/EngineeringTeamPage';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<EngineeringTeamPage />} />
      </Routes>
    </div>
  );
}

export default App;
