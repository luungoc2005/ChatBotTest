import {
  GET_RESPONSE_REQUEST,
  GET_RESPONSE_SUCCESS,
  GET_RESPONSE_FAILURE,
} from './actionTypes';


const initialState = {
  text: '',
  response: {
    isLoading: false,
    payload: null,
    error: null,
  }
}

function homeReducer(state = initialState, action) {
  switch (action.type) {
    case GET_RESPONSE_REQUEST:
      return {
        ...state,
        text: action.text,
        response: {
          ...state.response,
          isLoading: true,
          error: null,
        }
      }

    case GET_RESPONSE_SUCCESS:
      return {
        ...state,
        response: {
          ...state.response,
          isLoading: false,
          payload: action.payload,
          error: null,
        }
      }

    case GET_RESPONSE_FAILURE:
      return {
        ...state,
        response: {
          ...state.response,
          isLoading: false,
          error: action.payload,
        }
      }
    
    default:
      return state;
  }
}

export default homeReducer;