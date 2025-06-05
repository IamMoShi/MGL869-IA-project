import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home.jsx";
import {CATEGORY_MAP} from "./utils/helpers.js";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      {Object.entries(CATEGORY_MAP).map(([name, category]) => (
        <Route
          key={name}
          path={`/${name}`}
          element={<Home category={category} />}
        />
      ))}
        <Route path="*" element={<div>Page non trouvée</div>} />
    </Routes>
  );
}

export default App;
