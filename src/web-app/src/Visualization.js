import React, { Component } from 'react'
import * as d3 from 'd3'

/**
 * Visualization component that creates a bar chart that visualizes the top k books or authors in the database.
 * @returns {JSX.Element} RowChart component with div that contains the bar chart
 * @constructor loads props (type of visualization and api response data) and sets state variables
 */
class RowChart extends React.Component {
    constructor(props) {
        super(props);
        if (this.props.type === 'book') {
          this.state = {
            yAxisAttribute: "title",
            xAxisAttribute: "rating_count",
            width: 600,
            height: 600,
          }
        } else {
          this.state = {
            yAxisAttribute: "name",
            xAxisAttribute: "rating_count",
            width: 600,
            height: 600,
          }
        }

        this.chartRef = React.createRef();
        this.drawChart = this.drawChart.bind(this);
    }

    /**
     * Determines the max value from the given json objects.
     * @param arr - array of json objects
     * @param prop - key of value
     * @returns {number} - max value
     */
    getMax(arr, prop) {
        let max = 0;
        for (let i = 0; i < arr.length; i++) {
            if (parseInt(arr[i][prop]) > max)
                max = parseInt(arr[i][prop]);
        }
        return max;
    }

    /**
     * Function that draws the bar chart with d3.js functions.
     */
    drawChart() {
        let margin = {top: 20, right: 30, bottom: 40, left: 100},
                    width = this.state.width - margin.left - margin.right,
                    height = this.state.height - margin.top - margin.bottom;
        // append the svg object to the body of the page
        let svg = d3.select(".rowChart")
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform",
                "translate(" + margin.left + "," + margin.top + ")");
        // add X axis
        let x = d3.scaleLinear()
                .domain([0, this.getMax(this.props.data, 'rating_count')])
                .range([ 0, width]);
        svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .attr('class','axis x')
                .call(d3.axisBottom(x))
                .selectAll("text")
                .attr("transform", "translate(-10,0)rotate(-45)")
                .style("text-anchor", "end");
        // add Y axis
        let y = d3.scaleBand()
                .range([ 0, height ])
                .domain(this.props.data.map((d) =>  d[this.state.yAxisAttribute]))
                .padding(.1);
        svg.append("g")
                .attr('class','axis y')
                .call(d3.axisLeft(y))
                .selectAll("text")
                .attr("dy", null)
        // add Bars
        svg.selectAll("myRect")
                .data(this.props.data)
                .enter()
                .append("rect")
                .on('mouseover', function(){
                    d3.select(this).style('opacity', 0.5)
                 })
                .on('mouseout', function(){
                    d3.select(this).style('opacity', 1)
                 })
                .attr("x", x(0) )
                .attr("y", (d) => y(d[this.state.yAxisAttribute]))
                .attr("width", 0)
                .attr("height", y.bandwidth() -10 )
                .attr("fill", "#DF337D")
                .transition(d3.transition().duration(1000))
                .attr("width", (d) => x(d[this.state.xAxisAttribute]))
    }

    componentDidMount() {
        this.drawChart();
    }

    render() {
      return <div className="rowChart"></div>;
    }
}

export default RowChart