import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home.jsx";      // ta page d’accueil
// import Upload from "./pages/Upload.jsx";
import PhotosGrid from "./components/PhotosGrid.jsx";  // ta page upload
import { CATEGORY_MAP } from './utils/categoryMap.js'; // ton fichier de mapping des catégories

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      {/*<Route path="/upload" element={<Upload />} />*/}

      {/* Routes dynamiques pour chaque catégorie */}
      {Object.entries(CATEGORY_MAP).map(([name, category]) => (
        <Route
          key={name}
          path={`/${name}`}
          element={<Home category={category} />}
        />
      ))}

      {/* Optionnel : une route pour gérer les 404 */}
      <Route path="*" element={<div>Page non trouvée</div>} />
    </Routes>
  );
}

export default App;
