import React from 'react';
import PropTypes from 'prop-types';
import PaginateComponent from '../Pagination';
import * as commitAPI from '../../api/CommitAPI';

const CommitList = React.forwardRef((props, ref) => {
  const { commits } = props;

  const url = window.location.href;

  React.useEffect(() => {
    commitAPI.getCommits(
      Object.fromEntries([
        ...(new URL(url)).searchParams.entries(),
      ]),
    );
  }, [url]);

  return (
    <div>
      {commits.length !== 0 && (
        <div>
          <div
            className="card card-outline-secondary mt-4 mb-3 w-100"
          >
            <div className="card-header">
              Commit List
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
                      {commit.author}
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
};

export default CommitList;
