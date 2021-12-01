import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';

const PaginateComponent = (props) => {
  const { paginate, params } = props;
  const { previous, next } = paginate;
  const { page } = params;

  const pageInt = parseInt(page, 10);
  let [first, second, third] = [0, 0, 0];

  const mountPath = (toPage) => {
    const query = new URLSearchParams({
      ...params, page: toPage,
    }).toString();
    return `/?${query}`;
  };

  if (!previous) {
    [first, second, third] = [1, 2, 3];
  } else if (!next) {
    [first, second, third] = [pageInt - 2, pageInt - 1, pageInt];
  } else if (previous && next) {
    [first, second, third] = [pageInt - 1, pageInt, pageInt + 1];
  }

  return (
    <nav aria-label="Page navigation example">
      <ul className="pagination justify-content-center mb-0">
        <li className={`page-item ${previous ? null : 'disabled'}`}>
          <Link className="page-link" to={mountPath(previous)}>❮</Link>
        </li>
        <li className={`page-item ${first === pageInt ? 'active' : null}`}>
          <Link className="page-link" to={mountPath(first)}>
            { first }
          </Link>
        </li>
        <li className={`page-item ${second === pageInt ? 'active' : null}`}>
          <Link className="page-link" to={mountPath(second)}>
            { second }
          </Link>
        </li>
        <li className={`page-item ${third === pageInt ? 'active' : null}`}>
          <Link className="page-link" to={mountPath(third)}>
            { third }
          </Link>
        </li>
        <li className={`page-item ${next ? null : 'disabled'}`}>
          <Link className="page-link" to={mountPath(next)}>❯</Link>
        </li>
      </ul>
    </nav>
  );
};

PaginateComponent.propTypes = {
  paginate: PropTypes.shape({
    previous: PropTypes.string,
    next: PropTypes.string,
    count: PropTypes.number,
  }).isRequired,
  params: PropTypes.objectOf(PropTypes.any).isRequired,
};

const mapStateToProps = (store) => ({
  paginate: store.commitState.commits_pagination,
  params: store.commitState.params,
});

export default connect(mapStateToProps)(PaginateComponent);
