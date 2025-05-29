import React, { useState } from 'react';
import './App.css';

const Header = () => {
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

    return (
        <header className="header">
            <div className="row-extended">
                <div className="logo">XPics</div>

                <div className="search-container">
                    <input type="text" placeholder="Rechercher..." />
                </div>

                <div className="buttons">
                    <button className="btn btn-secondary">Log in</button>
                    <button className="btn btn-secondary">Sign up</button>
                    <button className="btn btn-primary">Upload images</button>
                </div>
            </div>

            <div className="row">
                <div className="buttons">
                    <button className="btn btn-primary">All</button>
                    <button className="btn btn-primary">Sea</button>
                    <button className="btn btn-primary">Mountain</button>
                </div>
            </div>

            <div className="row-extended">
                <div className="buttons">
                    <div className="dropdown">
                        <button className="btn btn-menu" onClick={toggleDropdown}>
                            Menu
                        </button>
                        {isDropdownOpen && (
                            <ul className="dropdown-menu">
                                <li><a href="#">Accueil</a></li>
                                <li><a href="#">Profil</a></li>
                                <li><a href="#">Paramètres</a></li>
                                <li><a href="#">Déconnexion</a></li>
                            </ul>
                        )}
                    </div>
                    <div className="dropdown">
                        <button className="btn btn-menu" onClick={toggleDropdown}>
                            Menu
                        </button>
                        {isDropdownOpen && (
                            <ul className="dropdown-menu">
                                <li><a href="#">Accueil</a></li>
                                <li><a href="#">Profil</a></li>
                                <li><a href="#">Paramètres</a></li>
                                <li><a href="#">Déconnexion</a></li>
                            </ul>
                        )}
                    </div>
                    <button className="btn btn-primary">Export All</button>
                </div>
                <a>
                    1-100 à 1 000 000
                </a>
            </div>
        </header>
    );
};

const PhotosGrid = () => {
    const images = [
    'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmy.alfred.edu%2Fzoom%2F_images%2Ffoster-lake.jpg&f=1&nofb=1&ipt=7b62f28eab72741f3e28d8e8e7125101f9f6ed949e05a8fbeaf5ca6f19ab5cb8',
    'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmy.alfred.edu%2Fzoom%2F_images%2Ffoster-lake.jpg&f=1&nofb=1&ipt=7b62f28eab72741f3e28d8e8e7125101f9f6ed949e05a8fbeaf5ca6f19ab5cb8',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmy.alfred.edu%2Fzoom%2F_images%2Ffoster-lake.jpg&f=1&nofb=1&ipt=7b62f28eab72741f3e28d8e8e7125101f9f6ed949e05a8fbeaf5ca6f19ab5cb8',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmy.alfred.edu%2Fzoom%2F_images%2Ffoster-lake.jpg&f=1&nofb=1&ipt=7b62f28eab72741f3e28d8e8e7125101f9f6ed949e05a8fbeaf5ca6f19ab5cb8',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmy.alfred.edu%2Fzoom%2F_images%2Ffoster-lake.jpg&f=1&nofb=1&ipt=7b62f28eab72741f3e28d8e8e7125101f9f6ed949e05a8fbeaf5ca6f19ab5cb8',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmy.alfred.edu%2Fzoom%2F_images%2Ffoster-lake.jpg&f=1&nofb=1&ipt=7b62f28eab72741f3e28d8e8e7125101f9f6ed949e05a8fbeaf5ca6f19ab5cb8',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmy.alfred.edu%2Fzoom%2F_images%2Ffoster-lake.jpg&f=1&nofb=1&ipt=7b62f28eab72741f3e28d8e8e7125101f9f6ed949e05a8fbeaf5ca6f19ab5cb8',
        'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fmy.alfred.edu%2Fzoom%2F_images%2Ffoster-lake.jpg&f=1&nofb=1&ipt=7b62f28eab72741f3e28d8e8e7125101f9f6ed949e05a8fbeaf5ca6f19ab5cb8',

    ];
    return (
        <div>
            <text>Photos</text>
            <div className="grid-container">
                {images.map((src, index) => (
                    <img key={index} src={src} alt={`img-${index}`} className="grid-image" />
                ))}
            </div>
        </div>
    );
};


function App() {
  const [message, setMessage] = useState('');
  const [prediction, setPrediction] = useState('');

  const handleUpload = async () => {
    const res = await fetch('http://localhost:5000/upload', { method: 'POST' });
    const data = await res.json();
    setMessage(data.message);
  };

  // const handlePredict = async () => {
  //   const res = await fetch('http://localhost:5000/api/images/predict', { method: 'POST' });
  //   const data = await res.json();
  //   setPrediction(data.prediction);
  // };

    return (
        <div className="App">
            <Header/>
            <PhotosGrid/>
            <h1>SmartVue Photos</h1>
            <button onClick={handleUpload}>Upload Image</button>
            <p>{message}</p>
            {/*<button onClick={handlePredict}>Predict Image</button>*/}
            {/*<p>{prediction}</p>*/}
        </div>
    );
}

export default App;