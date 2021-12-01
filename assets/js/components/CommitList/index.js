import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import PaginateComponent from '../Pagination';
import * as commitAPI from '../../api/CommitAPI';

const CommitList = React.forwardRef((props, ref) => {
  const { commits, filterParams } = props;
  const url = window.location.href;

  React.useEffect(() => {
    const urlQueryData = Object.fromEntries([
      ...(new URL(url)).searchParams.entries(),
    ]);
    commitAPI.getCommits(urlQueryData);
  }, [url]);

  const updateQueryString = (filter, value) => {
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.set(filter, value);
    searchParams.set('page', '1');
    return `/?${searchParams.toString()}`;
  };

  return (
    <div>
      {commits.length !== 0 && (
        <div>
          <div
            className="card card-outline-secondary mt-4 mb-3 w-100"
          >
            <div className="card-header">
              Commit List
              {Object.keys(filterParams).filter((field) => field !== 'page').map((field) => (
                <span className="badge badge-dark float-right mt-1 mr-1">
                  {`${field.includes('author') ? 'author' : 'repository'}: ${filterParams[field]}`}
                </span>
              ))}
            </div>

            <div
              className="card-body"
              ref={ref}
              style={{ overflow: 'scroll', overflowX: 'hidden' }}
            >
              {commits.map((commit, index) => (
                <div key={commit.sha}>
                  <div className="avatar">
                    <img alt={commit.author} className="img-author" src={commit.avatar} />
                  </div>
                  <div className="commit-details">
                    <p>
                      {commit.message}
                    </p>
                    <small className="text-muted">
                      <Link to={updateQueryString('author', commit.author)}>
                        {commit.author}
                      </Link>
                      {' '}
                      authored
                      {' '}
                      on
                      {' '}
                      {commit.repository}
                      {' '}
                      at
                      {' '}
                      {commit.date}
                    </small>
                    {index !== commits.length - 1 && <hr />}
                  </div>
                </div>
              ))}
            </div>
          </div>
          <PaginateComponent />
        </div>
      )}
    </div>
  );
});

CommitList.propTypes = {
  commits: PropTypes.arrayOf(PropTypes.object).isRequired,
  filterParams: PropTypes.objectOf(PropTypes.any).isRequired,
};

export default CommitList;
