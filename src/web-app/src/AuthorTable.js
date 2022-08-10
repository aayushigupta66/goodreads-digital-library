import React from 'react';

/**
 * Author table component that creates a table with author details for the viewer to easily read.
 * @param data - json data from the api response
 * @returns {JSX.Element} AuthorTable component with response details
 * @constructor NA
 */
const AuthorTable = ({ data }) => (
  <table>
    <thead>
      <tr>
        <th>Author URL</th>
        <th>Name</th>
        <th>Author ID</th>
        <th>Rating</th>
        <th>Rating Count</th>
        <th>Review Count</th>
        <th>Image URL</th>
        <th>Related Authors</th>
        <th>Author Books</th>
      </tr>
    </thead>
    <tbody>
      {data.map(elem => (
        <tr>
          <td key={elem._id}>{elem.author_url}</td>
          <td key={elem._id}>{elem.name}</td>
          <td key={elem._id}>{elem.id}</td>
          <td key={elem._id}>{elem.rating}</td>
          <td key={elem._id}>{elem.rating_count}</td>
          <td key={elem._id}>{elem.review_count}</td>
          <td key={elem._id}>{elem.image_url}</td>
          <td key={elem._id}>{elem.related_authors}</td>
          <td key={elem._id}>{elem.author_books}</td>
        </tr>
      ))}
    </tbody>
  </table>
)

export default AuthorTable