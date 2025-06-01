import MainLayout from "./components/MainLayout.jsx";

function App({children}) {

    return (
        <html lang="en">
        <body>
        <MainLayout>{children}</MainLayout>
        </body>
        </html>
    );
}

export default App
