port module Main exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (..)
import Json.Decode as D
import String exposing (..)
import Dropdown



-- MAIN


main : Program () Model Msg
main =
  Browser.element
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    }




-- PORTS


port sendMessage : String -> Cmd msg
port messageReceiver : (String -> msg) -> Sub msg



-- MODEL


type alias Model =
  { draft : String
  , messages : List String
  , selectedValue : Maybe String
  }


init : () -> ( Model, Cmd Msg )
init flags =
  ( { draft = "bubble", messages = [], selectedValue = Nothing }
  , Cmd.none
  )



-- UPDATE


type Msg
  = Send
  | Recv String
  | NoOp
  | DropdownChanged (Maybe String)


-- Use the `sendMessage` port when someone presses ENTER or clicks
-- the "Send" button. Check out index.html to see the corresponding
-- JS where this is piped into a WebSocket.
--
update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    Send ->
      ( model
      , sendMessage model.draft
      )

    Recv message ->
      ( { model | messages = [message] }
      , Cmd.none
      )

    DropdownChanged selectedValue ->
      ( { model | draft = Maybe.withDefault "bubble" selectedValue }
      , Cmd.none
      )

    NoOp ->
      ( model 
      , Cmd.none
      )



-- SUBSCRIPTIONS


-- Subscribe to the `messageReceiver` port to hear about messages coming in
-- from JS. Check out the index.html file to see how this is hooked up to a
-- WebSocket.
--
subscriptions : Model -> Sub Msg
subscriptions _ =
  messageReceiver Recv



-- VIEW

dropdownOptions : Dropdown.Options Msg
dropdownOptions =
    let
        defaultOptions =
            Dropdown.defaultOptions DropdownChanged
    in
    { defaultOptions
        | items =
            [ { value = "bubble", text = "Bubble Sort", enabled = True }
            , { value = "selection", text = "Selection Sort", enabled = True }
            , { value = "merge", text = "Merge Sort", enabled = True }
            ]
    }


-- view : Model -> Html Msg
-- view model =
--   div [ ]
--     [ h1 [] [ text "Elm Websocket Demo" ]
--     , Html.form []
--         [ p []
--             [ label []
--                 [ text "Sorting Algorithm: "
--                 , Dropdown.dropdown
--                     dropdownOptions
--                     []
--                     model.selectedValue
--                 ]
--               , button [ onClick Send ] [ text "Go!" ]
--             ]
--         ]
--     , div []
--         (List.map (\msg -> h4 [] [ text msg ]) model.messages)
--     ]

view : Model -> Html Msg
view model =
  div [ ]
    [ h1 [] [ text "Elm Websocket Demo" ]
    , p[] 
      [ text "Generates a random array and sorts it using algorithm of your choice through a Python Websocket server" ]
    , h4 [ ]
      [ label []
        [ text "Sorting Algorithm: "
        , Dropdown.dropdown
          dropdownOptions
          []
          model.selectedValue
        ]
        , button [ onClick Send ] [ text "Go!" ]
      ]
    , pre [ class "sort"]
        (List.map (\msg -> h4 [] [ text msg ]) model.messages)
    ]



-- DETECT ENTER


-- ifIsEnter : msg -> D.Decoder msg
-- ifIsEnter msg =
--   D.field "key" D.string
--     |> D.andThen (\key -> if key == "Enter" then D.succeed msg else D.fail "some other key")
