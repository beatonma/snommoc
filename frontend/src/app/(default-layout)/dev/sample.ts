import {
  Constituency,
  MemberMiniSchema,
  MemberProfile,
  PartyDetail,
} from "@/api/schema";

export const LabourParty: PartyDetail = {
  parliamentdotuk: 15,
  name: "Labour",
  short_name: null,
  long_name: null,
  homepage: "https://labour.org.uk/",
  year_founded: 1900,
  wikipedia: "https://en.wikipedia.org/wiki/Labour_Party_(UK)",
  logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
  logo_mask: null,
  active_member_count: 589,
  gender_demographics: [
    {
      modified_at: "2024-12-02T13:17:31.452Z",
      house: "Commons",
      male_member_count: 216,
      female_member_count: 186,
      non_binary_member_count: 0,
      total_member_count: 402,
    },
    {
      modified_at: "2024-12-02T13:17:33.193Z",
      house: "Lords",
      male_member_count: 113,
      female_member_count: 74,
      non_binary_member_count: 0,
      total_member_count: 187,
    },
  ],
  lords_demographics: {
    modified_at: "2024-12-02T13:17:35.045Z",
    life_count: 183,
    hereditary_count: 4,
    bishop_count: 0,
    total_count: 187,
  },
  theme: {
    primary: "rgb(213 0 0)",
    on_primary: "rgb(255 255 255)",
    accent: "rgb(213 213 0)",
    on_accent: "rgb(0 0 0)",
  },
};

export const KeirStarmerItem: MemberMiniSchema = {
  parliamentdotuk: 4514,
  name: "Keir Starmer",
  portrait: {
    fullsize_url:
      "https://members-api.parliament.uk/api/Members/4514/Portrait?cropType=FullSize",
    square_url:
      "https://members-api.parliament.uk/api/Members/4514/Portrait?cropType=OneOne",
    tall_url:
      "https://members-api.parliament.uk/api/Members/4514/Portrait?cropType=ThreeFour",
    wide_url:
      "https://members-api.parliament.uk/api/Members/4514/Portrait?cropType=ThreeTwo",
  },
  current_posts: [
    "Prime Minister and First Lord of the Treasury",
    "Leader of the Labour Party",
  ],
  party: {
    parliamentdotuk: 15,
    theme: {
      primary: "#d50000",
      on_primary: "#ffffff",
      accent: "#d5d500",
      on_accent: "#000000",
    },
    name: "Labour",
    logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
    logo_mask: null,
    active_member_count: 589,
    active_commons_members: null,
  },
  constituency: {
    parliamentdotuk: 4105,
    name: "Holborn and St Pancras",
    start: "2024-05-31",
    end: null,
  },
  lord_type: null,
};

export const KeirStarmerDetail: MemberProfile = {
  parliamentdotuk: 4514,
  name: "Keir Starmer",
  portrait: {
    full: "https://members-api.parliament.uk/api/Members/4514/Portrait?cropType=FullSize",
    square:
      "https://members-api.parliament.uk/api/Members/4514/Portrait?cropType=OneOne",
    wide: "https://members-api.parliament.uk/api/Members/4514/Portrait?cropType=ThreeTwo",
    tall: "https://members-api.parliament.uk/api/Members/4514/Portrait?cropType=ThreeFour",
  },
  current_posts: [
    "Prime Minister and First Lord of the Treasury",
    "Leader of the Labour Party",
  ],
  party: {
    parliamentdotuk: 15,
    theme: {
      primary: "#d50000",
      on_primary: "#ffffff",
      accent: "#d5d500",
      on_accent: "#000000",
    },
    name: "Labour",
    logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
    logo_mask: null,
    active_member_count: 589,
    active_commons_members: null,
  },
  constituency: {
    parliamentdotuk: 4105,
    name: "Holborn and St Pancras",
    start: "2024-05-31",
    end: null,
    mp: {
      parliamentdotuk: 4514,
      name: "Keir Starmer",
      party: {
        parliamentdotuk: 15,
        theme: {
          primary: "#d50000",
          on_primary: "#ffffff",
          accent: "#d5d500",
          on_accent: "#000000",
        },
        name: "Labour",
        logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
        logo_mask: null,
        active_member_count: 589,
        active_commons_members: null,
      },
    },
  },
  lord_type: null,
  full_title: "Rt Hon Sir Keir Starmer MP",
  status: {
    is_current: true,
    is_active: true,
    description: null,
    extra_notes: null,
    since: "2015-05-07",
  },
  house: "Commons",
  date_of_birth: null,
  date_of_death: null,
  age: 0,
  gender: "M",
  place_of_birth: null,
  current_committees: [],
  address: {
    physical: [
      {
        description: null,
        address: "House of Commons, London",
        postcode: "SW1A 0AA",
        phone: null,
        fax: null,
        email: "keir.starmer.mp@parliament.uk",
      },
      {
        description: null,
        address: "Constituency Office",
        postcode: null,
        phone: null,
        fax: null,
        email: "keir.starmer.constituency@parliament.uk",
      },
    ],
    web: [
      {
        url: "https://contact.no10.gov.uk/",
        description: null,
      },
      {
        url: "http://www.keirstarmer.com/",
        description: null,
      },
      {
        url: "https://twitter.com/keir_starmer",
        description: null,
      },
    ],
  },
  wikipedia: "https://en.wikipedia.org/wiki/Keir_Starmer",
};

export const InvernessConstituency: Constituency = {
  parliamentdotuk: 4483,
  name: "Inverness, Skye and West Ross-shire",
  start: "2024-05-31",
  end: null,
  mp: {
    parliamentdotuk: 5362,
    name: "Angus MacDonald",
    current_posts: [],
    party: {
      parliamentdotuk: 17,
      name: "Liberal Democrat",
      logo: null,
      logo_mask: null,
      theme: {
        primary: "rgb(250 160 26)",
        on_primary: "rgb(0 0 0)",
        accent: "rgb(255 255 255)",
        on_accent: "rgb(0 0 0)",
      },
      active_member_count: 150,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4483,
      name: "Inverness, Skye and West Ross-shire",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
    portrait: null,
  },
  boundary: null, // removed
  results: [
    {
      election: {
        parliamentdotuk: 422,
        name: "2024 General Election",
        date: "2024-07-04",
        election_type: null,
      },
      winner: {
        parliamentdotuk: 5362,
        name: "Angus MacDonald",
        current_posts: [],
        party: {
          parliamentdotuk: 17,
          name: "Liberal Democrat",
          logo: null,
          logo_mask: null,
          theme: {
            primary: "rgb(250 160 26)",
            on_primary: "rgb(0 0 0)",
            accent: "rgb(255 255 255)",
            on_accent: "rgb(0 0 0)",
          },
          active_member_count: 150,
          active_commons_members: null,
        },
        constituency: {
          parliamentdotuk: 4483,
          name: "Inverness, Skye and West Ross-shire",
          start: "2024-05-31",
          end: null,
        },
        lord_type: null,
        portrait: null,
      },
      electorate: 77927,
      turnout: 48056,
      result: "LD Gain",
      majority: 2160,
      candidates: [
        {
          name: "Angus MacDonald",
          profile: {
            parliamentdotuk: 5362,
            name: "Angus MacDonald",
            current_posts: [],
            party: {
              parliamentdotuk: 17,
              name: "Liberal Democrat",
              logo: null,
              logo_mask: null,
              theme: {
                primary: "rgb(250 160 26)",
                on_primary: "rgb(0 0 0)",
                accent: "rgb(255 255 255)",
                on_accent: "rgb(0 0 0)",
              },
              active_member_count: 150,
              active_commons_members: null,
            },
            constituency: {
              parliamentdotuk: 4483,
              name: "Inverness, Skye and West Ross-shire",
              start: "2024-05-31",
              end: null,
            },
            lord_type: null,
            portrait: null,
          },
          party: {
            parliamentdotuk: 17,
            name: "Liberal Democrat",
            logo: null,
            logo_mask: null,
            theme: {
              primary: "rgb(250 160 26)",
              on_primary: "rgb(0 0 0)",
              accent: "rgb(255 255 255)",
              on_accent: "rgb(0 0 0)",
            },
            active_member_count: 150,
            active_commons_members: null,
          },
          order: 1,
          votes: 18159,
        },
        {
          name: "Darren Paxton",
          profile: null,
          party: {
            parliamentdotuk: 144,
            name: "Socialist Equality Party",
            logo: null,
            logo_mask: null,
            theme: null,
            active_member_count: 0,
            active_commons_members: null,
          },
          order: 7,
          votes: 178,
        },
        {
          name: "Dillan Hill",
          profile: null,
          party: {
            parliamentdotuk: 1036,
            name: "Reform UK",
            logo: null,
            logo_mask: null,
            theme: {
              primary: "rgb(18 182 207)",
              on_primary: "rgb(255 255 255)",
              accent: "rgb(255 255 255)",
              on_accent: "rgb(0 0 0)",
            },
            active_member_count: 5,
            active_commons_members: null,
          },
          order: 4,
          votes: 2934,
        },
        {
          name: "Drew Hendry",
          profile: null,
          party: {
            parliamentdotuk: 29,
            name: "SNP",
            logo: null,
            logo_mask: null,
            theme: {
              primary: "rgb(255 246 133)",
              on_primary: "rgb(0 0 0)",
              accent: "rgb(255 255 255)",
              on_accent: "rgb(0 0 0)",
            },
            active_member_count: 9,
            active_commons_members: null,
          },
          order: 2,
          votes: 15999,
        },
        {
          name: "Michael Perera",
          profile: null,
          party: {
            parliamentdotuk: 15,
            name: "Labour",
            logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
            logo_mask: null,
            theme: {
              primary: "rgb(213 0 0)",
              on_primary: "rgb(255 255 255)",
              accent: "rgb(213 213 0)",
              on_accent: "rgb(0 0 0)",
            },
            active_member_count: 589,
            active_commons_members: null,
          },
          order: 3,
          votes: 6246,
        },
        {
          name: "Peter Newman",
          profile: null,
          party: {
            parliamentdotuk: 1057,
            name: "Scottish Green Party",
            logo: null,
            logo_mask: null,
            theme: {
              primary: "rgb(120 184 42)",
              on_primary: "rgb(255 255 255)",
              accent: "rgb(255 255 255)",
              on_accent: "rgb(0 0 0)",
            },
            active_member_count: 0,
            active_commons_members: null,
          },
          order: 6,
          votes: 2038,
        },
        {
          name: "Ruraidh Stewart",
          profile: null,
          party: {
            parliamentdotuk: 4,
            name: "Conservative",
            logo: "/media/party_logo/ic_party_conservative_t6WLgBs.svg",
            logo_mask:
              "/media/party_logo_mask/ic_party_conservative_mask_iem19G6.svg",
            theme: {
              primary: "rgb(0 99 186)",
              on_primary: "rgb(255 255 255)",
              accent: "rgb(255 255 255)",
              on_accent: "rgb(0 0 0)",
            },
            active_member_count: 394,
            active_commons_members: null,
          },
          order: 5,
          votes: 2502,
        },
      ],
    },
  ],
};

export const MemberList: MemberMiniSchema[] = [
  {
    parliamentdotuk: 5131,
    name: "Jack Abbott",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/5131/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/5131/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/5131/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/5131/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 100015,
      theme: {
        primary: "#51008a",
        on_primary: "#ffffff",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Labour (Co-op)",
      logo: null,
      logo_mask: null,
      active_member_count: 0,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4117,
      name: "Ipswich",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 172,
    name: "Diane Abbott",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/172/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/172/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/172/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/172/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4074,
      name: "Hackney North and Stoke Newington",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 3898,
    name: "Lord Aberdare",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/3898/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/3898/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/3898/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/3898/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 6,
      theme: {
        primary: "#c0c0c0",
        on_primary: "#000000",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Crossbench",
      logo: null,
      logo_mask: null,
      active_member_count: 184,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Excepted Hereditary",
  },
  {
    parliamentdotuk: 4212,
    name: "Debbie Abrahams",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/4212/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/4212/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/4212/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/4212/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4230,
      name: "Oldham East and Saddleworth",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 5120,
    name: "Shockat Adam",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/5120/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/5120/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/5120/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/5120/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 8,
      theme: {
        primary: "#909090",
        on_primary: "#ffffff",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Independent",
      logo: null,
      logo_mask: null,
      active_member_count: 15,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4142,
      name: "Leicester South",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 631,
    name: "Baroness Adams of Craigielea",
    portrait: null,
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
  {
    parliamentdotuk: 3453,
    name: "Lord Addington",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/3453/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/3453/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/3453/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/3453/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 17,
      theme: {
        primary: "#faa01a",
        on_primary: "#000000",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Liberal Democrat",
      logo: null,
      logo_mask: null,
      active_member_count: 150,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Excepted Hereditary",
  },
  {
    parliamentdotuk: 2175,
    name: "Lord Adebowale",
    portrait: null,
    current_posts: [],
    party: {
      parliamentdotuk: 6,
      theme: {
        primary: "#c0c0c0",
        on_primary: "#000000",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Crossbench",
      logo: null,
      logo_mask: null,
      active_member_count: 184,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
  {
    parliamentdotuk: 3743,
    name: "Lord Adonis",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/3743/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/3743/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/3743/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/3743/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
  {
    parliamentdotuk: 4689,
    name: "Lord Agnew of Oulton",
    portrait: null,
    current_posts: [],
    party: {
      parliamentdotuk: 4,
      theme: {
        primary: "#0063ba",
        on_primary: "#ffffff",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Conservative",
      logo: "/media/party_logo/ic_party_conservative_t6WLgBs.svg",
      logo_mask:
        "/media/party_logo_mask/ic_party_conservative_mask_iem19G6.svg",
      active_member_count: 394,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
  {
    parliamentdotuk: 4210,
    name: "Lord Ahmad of Wimbledon",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/4210/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/4210/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/4210/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/4210/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 4,
      theme: {
        primary: "#0063ba",
        on_primary: "#ffffff",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Conservative",
      logo: "/media/party_logo/ic_party_conservative_t6WLgBs.svg",
      logo_mask:
        "/media/party_logo_mask/ic_party_conservative_mask_iem19G6.svg",
      active_member_count: 394,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
  {
    parliamentdotuk: 5213,
    name: "Zubir Ahmed",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/5213/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/5213/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/5213/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/5213/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4477,
      name: "Glasgow South West",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 5112,
    name: "Luke Akehurst",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/5112/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/5112/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/5112/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/5112/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4204,
      name: "North Durham",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 5312,
    name: "Sadik Al-Hassan",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/5312/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/5312/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/5312/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/5312/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4214,
      name: "North Somerset",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 5097,
    name: "Bayo Alaba",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/5097/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/5097/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/5097/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/5097/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4316,
      name: "Southend East and Rochford",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 3478,
    name: "Lord Alderdice",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/3478/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/3478/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/3478/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/3478/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 17,
      theme: {
        primary: "#faa01a",
        on_primary: "#000000",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Liberal Democrat",
      logo: null,
      logo_mask: null,
      active_member_count: 150,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
  {
    parliamentdotuk: 5172,
    name: "Dan Aldridge",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/5172/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/5172/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/5172/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/5172/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4396,
      name: "Weston-super-Mare",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 4038,
    name: "Heidi Alexander",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/4038/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/4038/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/4038/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/4038/Portrait?cropType=ThreeTwo",
    },
    current_posts: ["Minister of State (Ministry of Justice)"],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4352,
      name: "Swindon South",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 632,
    name: "Douglas Alexander",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/632/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/632/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/632/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/632/Portrait?cropType=ThreeTwo",
    },
    current_posts: ["Minister of State (Department for Business and Trade)"],
    party: {
      parliamentdotuk: 100015,
      theme: {
        primary: "#51008a",
        on_primary: "#ffffff",
        accent: "#ffffff",
        on_accent: "#000000",
      },
      name: "Labour (Co-op)",
      logo: null,
      logo_mask: null,
      active_member_count: 0,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 4485,
      name: "Lothian East",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 4138,
    name: "Rushanara Ali",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/4138/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/4138/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/4138/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/4138/Portrait?cropType=ThreeTwo",
    },
    current_posts: [
      "Parliamentary Under-Secretary (Housing, Communities and Local Government)",
    ],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 3901,
      name: "Bethnal Green and Stepney",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 4747,
    name: "Tahir Ali",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/4747/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/4747/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/4747/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/4747/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: {
      parliamentdotuk: 3909,
      name: "Birmingham Hall Green and Moseley",
      start: "2024-05-31",
      end: null,
    },
    lord_type: null,
  },
  {
    parliamentdotuk: 397,
    name: "Lord Allan of Hallam",
    portrait: {
      fullsize_url:
        "https://members-api.parliament.uk/api/members/397/Portrait?cropType=FullSize",
      square_url:
        "https://members-api.parliament.uk/api/members/397/Portrait?cropType=OneOne",
      tall_url:
        "https://members-api.parliament.uk/api/members/397/Portrait?cropType=ThreeFour",
      wide_url:
        "https://members-api.parliament.uk/api/members/397/Portrait?cropType=ThreeTwo",
    },
    current_posts: [],
    party: {
      parliamentdotuk: 49,
      theme: null,
      name: "Non-affiliated",
      logo: null,
      logo_mask: null,
      active_member_count: 43,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
  {
    parliamentdotuk: 4304,
    name: "Lord Allen of Kensington",
    portrait: null,
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
  {
    parliamentdotuk: 3482,
    name: "Lord Alli",
    portrait: null,
    current_posts: [],
    party: {
      parliamentdotuk: 15,
      theme: {
        primary: "#d50000",
        on_primary: "#ffffff",
        accent: "#d5d500",
        on_accent: "#000000",
      },
      name: "Labour",
      logo: "/media/party_logo/ic_party_labour_8EBTZFj.svg",
      logo_mask: null,
      active_member_count: 589,
      active_commons_members: null,
    },
    constituency: null,
    lord_type: "Life peer",
  },
];
