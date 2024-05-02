import React from "react";
import { Chart as ChartJS } from "chart.js/auto";
import {Line} from "react-chartjs-2";
import data1 from "./data";

function Graph(){
    return (
        <div>
            <Line 

                data ={{
                    labels : [2018,2019,2020,2021,2022,2023],
                    datasets: data1.map((item) => ({
                    label: item.id.toString(),
                    data: item.values,
                    curve : "natural",
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    // tension: 0.1
        }))
                }} 
            />
        </div>
    )
}
export default Graph;