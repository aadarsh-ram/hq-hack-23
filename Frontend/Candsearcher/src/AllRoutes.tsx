import * as React from 'react'
import { lazy, useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';

import Upload from './components/Upload/Upload';
import ResultsPage from './components/ResultsPage/ResultsPage';


const AllRoutes = () => {
    return ( 
        <Routes>
            <Route path="/results/:pdfid" element={<ResultsPage />} />
            <Route path="/upload" element={<Upload />} />
        </Routes>
    );
}

export default AllRoutes;
