import * as React from 'react'
import { lazy, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';

import Upload from './components/Upload/Upload';
import ResultsPage from './components/ResultsPage/ResultsPage';
import ViewUploads from './components/ViewUploads/ViewUploads';
import Home from './components/HomePage/Home';


const AllRoutes = () => {
    return ( 
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/results/:pdfid" element={<ResultsPage />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/alluploads" element={<ViewUploads />} />
        </Routes>
    );
}

export default AllRoutes;