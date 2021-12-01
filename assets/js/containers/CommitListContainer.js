import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import CommitList from '../components/CommitList';

class CommitListContainer extends React.Component {
  constructor(props) {
    super(props);
    this.commitsContainer = React.createRef();
    this.setListSize = (component) => {
      const { innerHeight: height } = window;
      const { current: commitsContainer } = component;
      if (commitsContainer) {
        commitsContainer.style.height = commitsContainer && `${height - 210}px`;
      }
    };
  }

  componentDidMount() {
    // commitAPI.getCommits();
    window.addEventListener('resize', () => this.setListSize(this.commitsContainer));
    setTimeout(() => this.setListSize(this.commitsContainer), 200);
  }

  render() {
    const { commits, filterParams } = this.props;
    return (
      <CommitList
        ref={this.commitsContainer}
        commits={commits}
        filterParams={filterParams}
      />
    );
  }
}

CommitListContainer.propTypes = {
  commits: PropTypes.arrayOf(PropTypes.object).isRequired,
  filterParams: PropTypes.objectOf(PropTypes.any).isRequired,
};

const mapStateToProps = (store) => ({
  commits: store.commitState.commits,
  filterParams: store.commitState.params,
});

export default connect(mapStateToProps)(CommitListContainer);
