import React  from "react";
import '../styles/Home.css';

import Header from "../components/layout/Header";
import ImageGridInfinityScrolling from "../components/images/listing/ImageGridInfinityScrolling.tsx";

function Home({ category }) {
    return (
        <div className="App">
            <Header category={category}/>
            <ImageGridInfinityScrolling category={category}/>
        </div>
    );
}

export default Home;