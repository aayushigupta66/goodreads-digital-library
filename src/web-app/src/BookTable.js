import React from 'react';

/**
 * Book table component that creates a table with book details for the viewer to easily read.
 * @param data - json data from the api response
 * @returns {JSX.Element} BookTable component with response details
 * @constructor NA
 */
const BookTable = ({ data }) => (
  <table>
    <thead>
      <tr>
        <th>Book URL</th>
        <th>Title</th>
        <th>Book ID</th>
        <th>ISBN</th>
        <th>Author URL</th>
        <th>Author</th>
        <th>Rating</th>
        <th>Rating Count</th>
        <th>Review Count</th>
        <th>Image URL</th>
        <th>Similar Books</th>
      </tr>
    </thead>
    <tbody>
      {data.map(elem => (
        <tr>
          <td key={elem._id}>{elem.book_url}</td>
          <td key={elem._id}>{elem.title}</td>
          <td key={elem._id}>{elem.book_id}</td>
          <td key={elem._id}>{elem.ISBN}</td>
          <td key={elem._id}>{elem.author_url}</td>
          <td key={elem._id}>{elem.author}</td>
          <td key={elem._id}>{elem.rating}</td>
          <td key={elem._id}>{elem.rating_count}</td>
          <td key={elem._id}>{elem.review_count}</td>
          <td key={elem._id}>{elem.image_url}</td>
          <td key={elem._id}>{elem.similar_books}</td>
        </tr>
      ))}
    </tbody>
  </table>
)

export default BookTable