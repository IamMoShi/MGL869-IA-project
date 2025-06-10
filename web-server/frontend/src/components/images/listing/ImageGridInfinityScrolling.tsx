import React, {useEffect, useState, useRef, useCallback} from 'react';
import {Grid, Sheet, Typography} from "@mui/joy";
import {ID_TO_CATEGORY} from "../../../utils/helpers";
import ImageCard from "./ImageCard";
import {LoadSpinner} from "../../common/LoadSpinner";
import {IoIosArrowUp} from "react-icons/io";

type Image = {
    url: string,
    category: number, filename: string
}
// @ts-ignore
export default  function  ImageGridInfinityScrolling  ({category})  {
    const [images, setImages] = useState<Image[]>([]);
    const [page, setPage] = useState<number>(1);
    const [hasMore, setHasMore] = useState<boolean>(true);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const [limit, setLimit] = useState(500);

    const observer = useRef<IntersectionObserver | null>(null);

    const fetchImages = async (pageNum: number) => {
        setLoading(true);

        try {
            let path = `http://localhost:8080/api/images?category=${category}&limit=${limit}&skip=${(page - 1) * limit}`;
            if (category === undefined) {
                path = `http://localhost:8080/api/images?limit=${limit}&skip=${(page - 1) * limit}`;
            }

            const res = await fetch(path);

            const data = await res.json();
            // @ts-ignore
            setImages((prev) => [...prev, ...data.images]);
            if (data.images.length < limit) {
                setHasMore(false);
            }
        } catch (err) {
            setError('An error occurred while fetching data.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchImages(page);
    }, [page]);


    const lastImageElementRef = useCallback(
        (node: HTMLDivElement) => {
            if (loading) return;
            if (observer.current) observer.current.disconnect();
            observer.current = new IntersectionObserver(
                (entries) => {
                    // @ts-ignore
                    if (entries[0].isIntersecting && hasMore) {
                        setPage((prevPage) => prevPage + 1);
                    }
                },
                {threshold: 1.0}
            );
            if (node) observer.current.observe(node);
        },
        [loading, hasMore]
    );


    return (
        <div className="p-4">
            <Sheet sx={{px: 10, py: 5}}>
                <Typography textAlign="right"
                            level="body-sm">{images.length} image{images.length <= 1 ? "" : "s"} trouvée{images.length <= 1 ? "" : "s"}</Typography>

                <Typography level="h2" sx={{mb: 2, pb: 2}}>
                    Photos {category !== undefined ? ` - ${ID_TO_CATEGORY[category]}` : ""}
                </Typography>

                <Grid container spacing={2}>
                    {images.map((image, index) => {
                        if (images.length === index + 1) {
                            return <Grid xs={12} sm={6} md={4} lg={3} key={index} ref={lastImageElementRef}>
                                <ImageCard imageUrl={image.url} category={image.category} fetchData={fetchImages}/>
                            </Grid>
                        } else {
                            return (<Grid xs={12} sm={6} md={4} lg={3} key={index}>
                                <ImageCard imageUrl={image.url} category={image.category} fetchData={fetchImages}/>
                            </Grid>);
                        }
                    })}
                </Grid>
                <div className="fixed bottom-4 right-4 floating-btn">
                    <button
                        onClick={() => window.scrollTo({top: 0, behavior: 'smooth'})}
                        className="bg-blue-500 hover:bg-blue-600
                       text-white font-bold py-5 px-6
                       rounded-full shadow-lg hover:shadow-xl
                       transition duration-300 ease-in-out
                       transform hover:scale-110 bounce relative">
                        <IoIosArrowUp size={18}/>
                    </button>
                    <span className="tooltip">Scroll to Top</span>
                </div>
            </Sheet>
            {!hasMore &&
                <p className="text-center text-gray-500 text-3xl font-bold py-4">{images.length} image{images.length <= 1 ? "" : "s"} trouvée{images.length <= 1 ? "" : "s"}</p>}
            {loading && <div className="text-center py-4"><LoadSpinner/></div>}
            {error && <p className="text-center text-red-500 py-4">{error}</p>}
        </div>
    );
}